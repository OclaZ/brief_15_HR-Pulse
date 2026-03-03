from fastapi.testclient import TestClient
import io
from unittest.mock import patch

# On importe ton application FastAPI
from main import app

client = TestClient(app)

# On simule (mock) le pipeline pour éviter l'erreur 500 si le fichier .pkl est absent
@patch("main.salary_pipeline")
def test_predict_salary_success(mock_pipeline):
    """Test de la route de prédiction avec Mocking du modèle ML"""
    
    # On configure le faux modèle pour renvoyer toujours 100.5
    mock_pipeline.predict.return_value = [100.5]
    
    payload = {
        "job_title": "Data Scientist",
        "location": "New York, NY",
        "rating": 4.2,
        "skills": ["python", "sql", "machine learning"]
    }
    
    response = client.post("/predict-salary", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_salary_k"] == 100.5

def test_predict_salary_missing_fields():
    """Test que l'API rejette les requêtes incomplètes (422)"""
    payload = {"rating": 4.2} # Manque Title et Location
    response = client.post("/predict-salary", json=payload)
    assert response.status_code == 422

def test_upload_csv_file():
    """Test de l'upload de fichier"""
    file_content = b"id,job_title,skills\n1,Data Scientist,python"
    test_file = io.BytesIO(file_content)
    test_file.name = "test_data.csv"
    
    response = client.post(
        "/upload",
        files={"file": ("test_data.csv", test_file, "text/csv")}
    )
    assert response.status_code == 200