from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_countries_all():
    response = client.get("/countries/all")
    assert response.status_code == 200
    assert len(response.json()) == 246

def test_countries_search():
    response = client.post("/countries/search", json={"search_term": "ANT"})
    assert response.status_code == 200
    assert response.json() == [{
        "code": "ATA",
        "description": "Antarctica"
    },
    {
        "code": "ATG",
        "description": "Antigua and Barbuda"
    },
    {
        "code": "ANT",
        "description": "Netherlands Antilles"
    }]
