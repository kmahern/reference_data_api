from pydantic import BaseModel


class CountryBase(BaseModel):
    code: str
    description: str | None = None


class CountryCreate(CountryBase):
    pass


class Country(CountryBase):
    id: int

    class Config:
        orm_mode = True

