from typing import Optional

from pydantic import BaseModel


class Airline(BaseModel):
    """Modèle pour les compagnies aériennes"""

    iata_code: str
    airline_name: str

    class Config:
        from_attributes = True


class Airport(BaseModel):
    """Modèle pour les aéroports"""

    iata_code: str
    airport_name: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True
