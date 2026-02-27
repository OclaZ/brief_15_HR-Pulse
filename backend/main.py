import os
import joblib
import pandas as pd
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine
from dotenv import load_dotenv 
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Charge les variables d'environnement
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "salary_predictor.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "ml", "models", "model_features.pkl")

# NOUVEAU : Connexion à la base de données Azure SQL
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# 1. Configuration de l'identité du service
resource = Resource(attributes={"service.name": "hr-pulse-backend"})
provider = TracerProvider(resource=resource)

# 2. Configuration de l'exportateur (vers Jaeger)
# S'il ne trouve pas la variable (ex: en local), il vise localhost par défaut
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI(title="HR-Pulse API")

FastAPIInstrumentor.instrument_app(app)

# Cela va chronométrer tes appels sortants vers Azure AI (car le SDK Azure utilise 'requests' en arrière-plan)
RequestsInstrumentor().instrument()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle
try:
    model = joblib.load(MODEL_PATH)
    model_features = joblib.load(FEATURES_PATH)
except Exception as e:
    print(f"⚠️ Erreur chargement modèle : {e}")

class SalaryPredictionRequest(BaseModel):
    rating: float
    skills: List[str]

class SalaryPredictionResponse(BaseModel):
    predicted_salary_k: float

@app.post("/predict-salary", response_model=SalaryPredictionResponse)
def predict_salary(request: SalaryPredictionRequest):
    try:
        input_data = {feature: 0 for feature in model_features}
        input_data['Rating'] = request.rating
        
        for skill in request.skills:
            skill_feature_name = f"skill_{skill.lower()}"
            if skill_feature_name in input_data:
                input_data[skill_feature_name] = 1
                
        df_input = pd.DataFrame([input_data])
        prediction = model.predict(df_input)[0]
        return SalaryPredictionResponse(predicted_salary_k=round(prediction, 2))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- LA ROUTE MODIFIÉE POUR AZURE SQL ---
@app.get("/jobs")
def get_jobs(limit: int = 10, skill: str = None):
    """Récupère les jobs depuis la base de données Azure SQL"""
    try:
        # On utilise Pandas pour exécuter la requête SQL sur notre moteur Azure
        # Dans main.py, route /jobs
        query = "SELECT id, job_title, skills_extracted, [Company Name] as company_name, Location as location, [Salary Estimate] as salary_estimate FROM jobs"
        df = pd.read_sql(query, engine)
        
        # Filtre optionnel par compétence
        if skill:
            df = df[df['skills_extracted'].str.lower().str.contains(skill.lower(), na=False)]
            
        return df.head(limit).to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à Azure SQL : {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(BASE_DIR, "ml", "data", f"uploaded_{file.filename}")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"message": f"Fichier '{file.filename}' chargé avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'upload : {str(e)}")