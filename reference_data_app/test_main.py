from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from .database import Base
from .main import app, get_db
from . import crud, schemas

import yaml

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def seed_test_data():
    db = TestingSessionLocal()
    with open("countries.yml", "r") as file:
        countries = yaml.safe_load(file)
        for country in countries:
            new_country = schemas.CountryCreate(
                code=country[":code"], description=country[":description"]
            )
            db_country = crud.get_country_by_code(db, code=new_country.code)
            if not db_country:
                crud.create_country(db=db, country=new_country)

def test_countries_all():
    seed_test_data()
    response = client.get("/countries/all")
    assert response.status_code == 200
    assert len(response.json()) == 246


def test_countries_search():
    response = client.post("/countries/search", json={"search_term": "ANT"})
    assert response.status_code == 200
    assert response.json() == [
        {"code": "ATA", "description": "Antarctica"},
        {"code": "ATG", "description": "Antigua and Barbuda"},
        {"code": "ANT", "description": "Netherlands Antilles"},
    ]
