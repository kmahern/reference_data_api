import yaml
import reference_data_app
from reference_data_app.database import SessionLocal
from reference_data_app import crud

db = SessionLocal()
print("Creating initial data")
with open("countries.yml", "r") as file:
    countries = yaml.safe_load(file)
for country in countries:
    new_country = reference_data_app.schemas.CountryCreate(
        code=country[":code"], description=country[":description"]
    )
    db_country = reference_data_app.crud.get_country_by_code(db, code=new_country.code)
    if not db_country:
        crud.create_country(db=db, country=new_country)
print("Initial data created")
