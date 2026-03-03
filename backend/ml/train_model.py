import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned-data.csv")

print("⏳ Chargement et préparation des données...")
df = pd.read_csv("data/cleaned-data.csv")

# 1. Nettoyage de la note (Rating)
df['Rating'] = df['Rating'].replace(-1.0, np.nan)
df['Rating'] = df['Rating'].fillna(df['Rating'].median())

# 2. Extraction des compétences (Features binaires manuelles)
TECH_SKILLS = [
    "python", "sql", "aws", "machine learning", "deep learning", "hadoop", 
    "spark", "java", "c++", "tableau", "power bi", "excel", "nosql", 
    "azure", "gcp", "docker", "kubernetes", "nlp", "statistics", "tensorflow", "pytorch"
]

def extract_skills_list(description):
    desc = str(description).lower()
    return [skill for skill in TECH_SKILLS if skill in desc]

df['skills_list'] = df['Job Description'].apply(extract_skills_list)
for skill in TECH_SKILLS:
    df[f"skill_{skill}"] = df['skills_list'].apply(lambda x: 1 if skill in x else 0)

# 3. Sélection des Features
# On ajoute 'Job Title' et 'Location' pour utiliser le OneHotEncoder
categorical_features = ['Job Title', 'Location']
numeric_features = ['Rating'] + [f"skill_{skill}" for skill in TECH_SKILLS]

df = df.dropna(subset=['Average_Salary'] + categorical_features)

X = df[categorical_features + numeric_features]
y = df['Average_Salary']

# Séparation Train / Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- CONFIGURATION DU ONEHOTENCODER ---
# handle_unknown='ignore' est crucial pour ne pas planter si un nouveau titre de poste arrive en prod
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
        ('num', 'passthrough', numeric_features)
    ]
)

# --- CRÉATION DU PIPELINE ---
# Le pipeline enchaîne automatiquement l'encodage et l'entraînement
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
])

print("🧠 Entraînement du Pipeline (Encoding + Random Forest)...")
model_pipeline.fit(X_train, y_train)

# 4. Évaluation
print("\n📊 Performances du modèle :")
predictions = model_pipeline.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"🔹 MAE : ± {mae * 1000:,.2f} $")
print(f"🔹 R² (Précision) : {r2:.4f}")

# 5. Sauvegarde UNIQUE
# On sauvegarde le PIPELINE entier. Comme ça, en prod, tu n'as qu'à 
# charger un seul fichier qui s'occupe de l'encodage et de la prédiction.
joblib.dump(model_pipeline, "models/salary_pipeline.pkl")

print("\n✅ SUCCÈS : Le pipeline complet est sauvegardé sous 'models/salary_pipeline.pkl'")