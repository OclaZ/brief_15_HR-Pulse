import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

print("⏳ Chargement des données...")

# 1. On charge le fichier nettoyé complet (qui contient Company Name, Location, etc.)
# Assure-toi que le chemin correspond bien à ton dossier (ici "ml/data/cleaned-data.csv")
df_full = pd.read_csv("ml/data/cleaned-data.csv")

# 2. On charge le fichier avec les compétences extraites par l'IA
df_skills = pd.read_csv("ml/data/final-ds-jobs-azure.csv")

# On recrée la colonne 'id' sur le dataset complet pour pouvoir faire la correspondance
df_full['id'] = range(1, len(df_full) + 1)

# 3. On fusionne les deux tableaux grâce à l'ID
# On ajoute 'Company Name', 'Location' et 'Salary Estimate' aux données des skills
df_merged = pd.merge(
    df_skills, 
    df_full[['id', 'Company Name', 'Location', 'Salary Estimate']], 
    on='id', 
    how='left'
)

# 4. Connexion et envoi vers Azure SQL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("🚀 Mise à jour de la table 'jobs' sur Azure SQL en cours...")
# On remplace l'ancienne table par la nouvelle qui contient toutes les colonnes
df_merged.to_sql("jobs", con=engine, if_exists="replace", index=False)

print("✅ SUCCÈS : La base de données a été mise à jour avec les nouvelles colonnes !")