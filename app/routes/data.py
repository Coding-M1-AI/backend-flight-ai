from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Airline as AirlineModel, Airport as AirportModel
from app.schemas.data import Airline, Airport

router = APIRouter()

@router.get("/airlines", response_model=List[Airline])
async def get_airlines(db: Annotated[Session, Depends(get_db)]):
    """Récupérer la liste des compagnies aériennes depuis la base de données"""
    try:
        airlines_db = db.query(AirlineModel).order_by(AirlineModel.iata_code).all()

        # Vérifier s'il y a des données
        if not airlines_db:
            raise HTTPException(
                status_code=404,
                detail="Aucune compagnie aérienne trouvée. " \
                       "Exécutez 'python scripts/import_csv_to_db.py' pour importer les données.",
            )

        # Convertir en modèles Pydantic
        airlines = [Airline(iata_code=airline.iata_code, airline_name=airline.airline_name) for airline in airlines_db]

        return airlines

    except HTTPException:
        # Re-lancer les HTTPException existantes
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture des airlines: {str(e)}") from e


@router.get("/airports", response_model=List[Airport])
async def get_airports(db: Annotated[Session, Depends(get_db)]):
    """Récupérer la liste des aéroports depuis la base de données"""
    try:
        # Requête SQLAlchemy pour récupérer tous les aéroports
        airports_db = db.query(AirportModel).order_by(AirportModel.iata_code).all()

        # Vérifier s'il y a des données
        if not airports_db:
            raise HTTPException(
                status_code=404,
                detail="Aucun aéroport trouvé. Exécutez 'python scripts/import_csv_to_db.py' \
                       pour importer les données."
            )

        # Convertir en modèles Pydantic
        airports = [
            Airport(
                iata_code=airport.iata_code,
                airport_name=airport.airport_name,
                city=airport.city,
                state=airport.state,
                country=airport.country,
                latitude=airport.latitude,
                longitude=airport.longitude,
            )
            for airport in airports_db
        ]

        return airports

    except HTTPException:
        # Re-lancer les HTTPException existantes
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture des airports: {str(e)}") from e
