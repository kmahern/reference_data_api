from sqlalchemy.orm import Session

from . import models, schemas


def get_countries(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Country).offset(skip).limit(limit).all()

def get_country_by_code(db: Session, code: str):
    return db.query(models.Country).filter(models.Country.code == code).first()

def get_countries_by_search_term(search_term: str, db: Session, skip: int = 0, limit: int = 1000):
    search_term = "%{}%".format(search_term)
    return db.query(models.Country).filter(models.Country.description.like(search_term)).all()

def create_country(db: Session, country: schemas.CountryCreate):
    db_country = models.Country(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country
