from fastapi.testclient import TestClient
import io
from unittest.mock import patch, MagicMock

# On mock joblib.load AVANT d'importer l'app pour éviter l'erreur de chargement
with patch("joblib.load") as mock_load:
    # On crée un faux pipeline qui a une méthode predict
    mock_pipeline = MagicMock()
    mock_pipeline.predict.return_value = [105.0]
    mock_load.return_value = mock_pipeline
    
    # Maintenant on peut importer l'app sans que le try/except ne vide la variable
    from main import app

client = TestClient(app)

def test_predict_salary_success():
    """Test de la route de prédiction avec un mock global de joblib"""
    payload = {
        "job_title": "Data Scientist",
        "location": "New York, NY",
        "rating": 4.2,
        "skills": ["python", "sql", "machine learning"]
    }
    
    response = client.post("/predict-salary", json=payload)
    
    # Si ton main.py utilise 'salary_pipeline', le mock renverra 105.0
    assert response.status_code == 200
    data = response.json()
    assert "predicted_salary_k" in data

def test_predict_salary_missing_fields():
    """Vérifie que Pydantic bloque les requêtes incomplètes"""
    payload = {"rating": 4.5}
    response = client.post("/predict-salary", json=payload)
    assert response.status_code == 422

def test_upload_csv_file():
    """Test de la route d'upload"""
    file_content = b"id,job_title,skills\n1,Data Scientist,python"
    test_file = io.BytesIO(file_content)
    test_file.name = "test_data.csv"
    
    response = client.post(
        "/upload",
        files={"file": ("test_data.csv", test_file, "text/csv")}
    )
    assert response.status_code == 200