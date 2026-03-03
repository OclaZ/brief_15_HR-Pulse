from fastapi.testclient import TestClient
import io

# On importe ton application FastAPI depuis le fichier main.py
from main import app

# Création du client de test
client = TestClient(app)

def test_predict_salary_success():
    """Test de la route de prédiction avec le nouveau schéma (Job Title, Location, Rating, Skills)"""
    payload = {
        "job_title": "Data Scientist",
        "location": "New York, NY",
        "rating": 4.2,
        "skills": ["python", "sql", "machine learning"]
    }
    # Envoi de la requête POST vers l'endpoint de prédiction [cite: 56, 124]
    response = client.post("/predict-salary", json=payload)
    
    # On vérifie que la requête a réussi (Code 200) [cite: 85]
    assert response.status_code == 200
    
    # On vérifie que la réponse contient bien le salaire prédit par le pipeline [cite: 66, 118]
    data = response.json()
    assert "predicted_salary_k" in data
    assert isinstance(data["predicted_salary_k"], float)

def test_predict_salary_missing_fields():
    """Test que l'API rejette la requête s'il manque le titre ou la localisation (Erreur 422)"""
    payload = {
        "rating": 4.2,
        "skills": ["python"]
    }
    # Cette requête va échouer car job_title et location sont obligatoires pour le OneHotEncoder [cite: 90, 94]
    response = client.post("/predict-salary", json=payload)
    assert response.status_code == 422

def test_upload_csv_file():
    """Test de la route d'upload de fichiers CSV pour le recrutement [cite: 172]"""
    file_content = b"id,job_title,skills\n1,Data Scientist,python"
    test_file = io.BytesIO(file_content)
    test_file.name = "test_data.csv"
    
    response = client.post(
        "/upload",
        files={"file": ("test_data.csv", test_file, "text/csv")}
    )
    
    # Vérification du message de succès d'upload [cite: 173]
    assert response.status_code == 200
    assert "chargé avec succès" in response.json()["message"]