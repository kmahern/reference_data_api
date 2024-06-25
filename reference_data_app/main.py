from fastapi import Depends, FastAPI, HTTPException
from fastapi import Body
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/countries/", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_code(db, code=country.code)
    if db_country:
        raise HTTPException(status_code=400, detail="Country code already exists")
    return crud.create_country(db=db, country=country)


@app.post("/countries/search")
def search_countries(
    search_term: str = Body(embed=True),
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db),
):
    countries = crud.get_countries_by_search_term(
        search_term, db, skip=skip, limit=limit
    )
    countries_list = []
    for country in countries:
        countries_list.append(
            {"code": country.code, "description": country.description}
        )
    return countries_list


@app.get("/countries/all")
def read_countries(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    countries = crud.get_countries(db, skip=skip, limit=limit)
    countries_list = []
    for country in countries:
        countries_list.append(
            {"code": country.code, "description": country.description}
        )
    return countries_list
