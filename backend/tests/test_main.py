from fastapi.testclient import TestClient
import io

# On importe ton application FastAPI depuis le fichier main.py
from main import app

# Création du client de test
client = TestClient(app)

def test_predict_salary_success():
    """Test de la route de prédiction avec des données valides"""
    payload = {
        "rating": 4.2,
        "skills": ["python", "sql", "machine learning"]
    }
    response = client.post("/predict-salary", json=payload)
    
    # On vérifie que la requête a réussi (Code 200)
    assert response.status_code == 200
    
    # On vérifie que la réponse contient bien le salaire prédit
    data = response.json()
    assert "predicted_salary_k" in data
    assert isinstance(data["predicted_salary_k"], float)

def test_predict_salary_invalid_data():
    """Test de la barrière de sécurité Pydantic avec des données invalides"""
    payload = {
        "rating": "Quatre", # Erreur volontaire : on attend un float, on envoie une string
        "skills": ["python"]
    }
    response = client.post("/predict-salary", json=payload)
    
    # On vérifie que l'API rejette la requête (Code 422 - Unprocessable Entity)
    assert response.status_code == 422

def test_upload_csv_file():
    """Test de la route d'upload de fichiers"""
    # On simule un faux fichier CSV en mémoire
    file_content = b"id,job_title,skills\n1,Data Scientist,python"
    test_file = io.BytesIO(file_content)
    test_file.name = "test_data.csv"
    
    response = client.post(
        "/upload",
        files={"file": ("test_data.csv", test_file, "text/csv")}
    )
    
    # On vérifie que l'upload a fonctionné
    assert response.status_code == 200
    assert "chargé avec succès" in response.json()["message"]