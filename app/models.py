"""
Modèles de base de données SQLAlchemy
"""

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class FlightData(Base):
    """Modèle pour stocker les données de vol"""

    __tablename__ = "flight_data"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer, index=True)
    arrival_delay = Column(Float)
    raw_data = Column(Text)  # Stockage JSON des données brutes
    # func.now() est un callable SQLAlchemy, le type checker ne le reconnaît pas toujours
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PredictionResult(Base):
    """Modèle pour stocker les résultats de prédiction"""

    __tablename__ = "prediction_results"

    id = Column(Integer, primary_key=True, index=True)
    flight_data_id = Column(Integer, index=True)
    prediction_value = Column(Float)
    model_version = Column(String, default="v1.0")
    # func.now() est un callable SQLAlchemy, le type checker ne le reconnaît pas toujours
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Airline(Base):
    """Modèle pour stocker les données des compagnies aériennes"""

    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, index=True)
    iata_code = Column(String(3), unique=True, index=True, nullable=False)
    airline_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Airport(Base):
    """Modèle pour stocker les données des aéroports"""

    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    iata_code = Column(String(3), unique=True, index=True, nullable=False)
    airport_name = Column(String(255), nullable=False)
    city = Column(String(100))
    state = Column(String(50))
    country = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FlightRoute(Base):
    """Modèle pour stocker les routes de vol valides"""

    __tablename__ = "flight_routes"

    id = Column(Integer, primary_key=True, index=True)
    origin_airport_iata = Column(String(3), index=True, nullable=False)
    destination_airport_iata = Column(String(3), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
