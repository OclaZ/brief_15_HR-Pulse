import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

print("⏳ Chargement des données pour l'entraînement...")
df = pd.read_csv("data/cleaned-data.csv")

# 1. Nettoyage de la note d'entreprise (Rating)
df['Rating'] = df['Rating'].replace(-1.0, np.nan)
df['Rating'] = df['Rating'].fillna(df['Rating'].median())

# 2. Extraction des compétences (Features)
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

# 3. Définition des Features (X) et de la Target (y)
feature_cols = ['Rating'] + [f"skill_{skill}" for skill in TECH_SKILLS]

df = df.dropna(subset=['Average_Salary'])

X = df[feature_cols]
y = df['Average_Salary']

# --- NOUVEAU : Séparation Train / Test ---
# On garde 20% des données uniquement pour l'évaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraînement de l'algorithme "Random Forest" (sur X_train uniquement)
print("🧠 Entraînement de l'IA en cours (RandomForest)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- NOUVEAU : Évaluation du modèle (sur X_test) ---
print("\n📊 Évaluation des performances du modèle :")
predictions = model.predict(X_test)

# Calcul des métriques
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

# Affichage (On multiplie par 1000 car le salaire est en K$)
print(f"🔹 MAE (Erreur Absolue Moyenne) : ± {mae * 1000:,.2f} $")
print(f"🔹 RMSE (Erreur Quadratique Moyenne) : ± {rmse * 1000:,.2f} $")
print(f"🔹 R² (Score de précision) : {r2:.4f}")
print("-" * 50)

# 5. Sauvegarde du modèle et des noms de colonnes
# Tu peux choisir d'entraîner le modèle sur tout X une fois que tu es satisfait des métriques,
# mais ici on sauvegarde celui entraîné sur le Train set pour être cohérent.
joblib.dump(model, "models/salary_predictor.pkl")
joblib.dump(feature_cols, "models/model_features.pkl")

print("✅ SUCCÈS : Le modèle a été sauvegardé sous 'models/salary_predictor.pkl'")
print("✅ SUCCÈS : Les features ont été sauvegardées sous 'models/model_features.pkl'")