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

# [cite_start]Charge les variables d'environnement [cite: 46]
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# [cite_start]Chemin vers le pipeline complet (OneHotEncoder + RandomForest) [cite: 37, 39]
PIPELINE_PATH = os.path.join(BASE_DIR, "ml", "models", "salary_pipeline.pkl")

# [cite_start]Connexion à la base de données Azure SQL [cite: 26, 38]
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# [cite_start]--- Configuration Observabilité (Jaeger) --- [cite: 27]
resource = Resource(attributes={"service.name": "hr-pulse-backend"})
provider = TracerProvider(resource=resource)
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# [cite_start]Initialisation de l'API [cite: 46]
app = FastAPI(title="HR-Pulse API")

# [cite_start]Instrumentation pour le tracing [cite: 27]
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [cite_start]Chargement du Pipeline [cite: 37, 39]
try:
    salary_pipeline = joblib.load(PIPELINE_PATH)
except Exception as e:
    print(f"⚠️ Erreur chargement pipeline : {e}")

# Schéma Pydantic aligné sur le nouveau modèle (incluant Job Title et Location)
class SalaryPredictionRequest(BaseModel):
    job_title: str
    location: str
    rating: float
    skills: List[str]

class SalaryPredictionResponse(BaseModel):
    predicted_salary_k: float

@app.post("/predict-salary", response_model=SalaryPredictionResponse)
def predict_salary(request: SalaryPredictionRequest):
    """Prédit le salaire via le pipeline (OneHotEncoder automatique pour Title/Location)"""
    try:
        # Liste des skills de référence pour l'encodage binaire
        TECH_SKILLS = [
            "python", "sql", "aws", "machine learning", "deep learning", "hadoop", 
            "spark", "java", "c++", "tableau", "power bi", "excel", "nosql", 
            "azure", "gcp", "docker", "kubernetes", "nlp", "statistics", "tensorflow", "pytorch"
        ]

        # 1. Préparation du dictionnaire pour le DataFrame
        input_dict = {
            "Job Title": request.job_title,
            "Location": request.location,
            "Rating": request.rating
        }

        # 2. Encodage manuel des skills
        user_skills = [s.lower() for s in request.skills]
        for skill in TECH_SKILLS:
            input_dict[f"skill_{skill}"] = 1 if skill in user_skills else 0
                
        # 3. Conversion en DataFrame pour le ColumnTransformer du pipeline
        df_input = pd.DataFrame([input_dict])
        
        # [cite_start]4. Inférence (Le OneHotEncoder interne traite Title et Location) [cite: 39]
        prediction = salary_pipeline.predict(df_input)[0]
        
        return SalaryPredictionResponse(predicted_salary_k=round(float(prediction), 2))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs")
def get_jobs(limit: int = 10, skill: str = None):
    """Récupère les offres depuis Azure SQL [cite: 38]"""
    try:
        query = "SELECT id, job_title, skills_extracted, [Company Name] as company_name, Location as location, [Salary Estimate] as salary_estimate FROM jobs"
        df = pd.read_sql(query, engine)
        
        if skill:
            df = df[df['skills_extracted'].str.lower().str.contains(skill.lower(), na=False)]
            
        return df.head(limit).to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur SQL : {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Gestion de l'import de fichiers CSV"""
    try:
        file_location = os.path.join(BASE_DIR, "ml", "data", f"uploaded_{file.filename}")
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": f"Fichier '{file.filename}' chargé avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'upload : {str(e)}")