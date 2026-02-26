# backend/seed_db.py
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Charge la variable DATABASE_URL depuis ton fichier .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print("⏳ Connexion à Azure SQL en cours...")
try:
    # Création du moteur de connexion
    engine = create_engine(DATABASE_URL)
    
    # Lecture des données locales
    df = pd.read_csv("ml/data/final-ds-jobs-azure.csv")
    
    print("🚀 Injection des données dans la table 'jobs'...")
    # L'argument if_exists="replace" crée la table si elle n'existe pas
    df.to_sql("jobs", con=engine, if_exists="replace", index=False)
    
    print("✅ SUCCÈS : Données injectées dans Azure SQL avec succès !")
except Exception as e:
    print(f"⚠️ ERREUR : {e}")