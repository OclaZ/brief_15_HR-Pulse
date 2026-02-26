import time
import json
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from tqdm import tqdm
from dotenv import load_dotenv
import os

load_dotenv()
ENDPOINT = os.getenv("AZURE_ENDPOINT")
KEY = os.getenv("AZURE_KEY")
def authenticate_client():
    return TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def run_ner_extraction(data_path, output_path, limit=100):
    client = authenticate_client()
    
    # Chargement de notre dataset nettoyé
    df = pd.read_csv(data_path)

    # On traite seulement la limite demandée
    df_subset = df.head(limit).copy()
    all_skills = []

    print(f"🚀 Extraction des compétences pour {limit} offres via Azure NER...")

    # Traitement ligne par ligne pour éviter les limites de batch
    for i, row in tqdm(df_subset.iterrows(), total=len(df_subset)):
        # On limite à 1000 caractères pour optimiser et éviter les erreurs
        description = str(row["Job Description"])[:1000]  
        
        try:
            response = client.recognize_entities([description])
            doc = response[0]
            
            if not doc.is_error:
                # Les compétences pertinentes sont dans les catégories 'Skill' ou 'Product'
                skills = [
                    entity.text.lower() # Mis en minuscules pour la cohérence
                    for entity in doc.entities
                    if entity.category in ["Skill", "Product"]
                ]
                # Formatage en JSON comme exigé par le brief pour la DB
                all_skills.append(json.dumps(list(set(skills))))
            else:
                all_skills.append(json.dumps([]))
                
        except Exception as e:
            print(f"\n⚠️ Erreur à la ligne {i}: {e}")
            all_skills.append(json.dumps([]))

        # Pause pour respecter le Free Tier Azure
        time.sleep(1.0)

    # Ajout de la colonne avec le nom exact attendu par le brief
    df_subset["skills_extracted"] = all_skills
    
    # Création de l'ID unique et sélection des colonnes pour Azure SQL
    df_subset['id'] = range(1, len(df_subset) + 1)
    df_sql = df_subset[['id', 'job_title', 'skills_extracted']]
    
    # Sauvegarde
    df_sql.to_csv(output_path, index=False)
    print(f"\n✅ Extraction terminée. {len(df_subset)} lignes sauvegardées dans {output_path}")
    print(df_sql.head())

# Lancement du script
if __name__ == "__main__":
    # On utilise notre fichier nettoyé de la Phase 3
    run_ner_extraction("./data/cleaned-data.csv", "final-ds-jobs-azure.csv", limit=100)