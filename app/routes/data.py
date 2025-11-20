from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Airline as AirlineModel,
    Airport as AirportModel,
    FlightRoute as FlightRouteModel,
)
from app.schemas.data import Airline, Airport

router = APIRouter()


@router.get("/airlines", response_model=List[Airline])
async def get_airlines(db: Annotated[Session, Depends(get_db)]):
    """Récupérer la liste des compagnies aériennes depuis la base de données"""
    try:
        airlines_db = db.query(AirlineModel).order_by(AirlineModel.iata_code).all()

        if not airlines_db:
            raise HTTPException(
                status_code=404,
                detail="Aucune compagnie aérienne trouvée. "
                "Exécutez 'python scripts/import_csv_to_db.py' pour importer les données.",
            )

        airlines = [Airline.from_orm(airline) for airline in airlines_db]

        return airlines

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture des airlines: {str(e)}") from e


@router.get("/airports", response_model=List[Airport])
async def get_airports(db: Annotated[Session, Depends(get_db)]):
    """Récupérer la liste des aéroports depuis la base de données"""
    try:
        airports_db = db.query(AirportModel).order_by(AirportModel.iata_code).all()

        if not airports_db:
            raise HTTPException(
                status_code=404,
                detail="Aucun aéroport trouvé. Exécutez 'python scripts/import_csv_to_db.py' \
                       pour importer les données.",
            )

        airports = [Airport.from_orm(airport) for airport in airports_db]

        return airports

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture des airports: {str(e)}") from e


@router.get("/airports/destinations/{origin_iata_code}", response_model=List[Airport])
async def get_destinations_for_origin(origin_iata_code: str, db: Annotated[Session, Depends(get_db)]):
    """Récupérer la liste des aéroports de destination valides pour un aéroport d'origine donné"""
    try:
        destination_iatas = (
            db.query(FlightRouteModel.destination_airport_iata)
            .filter(FlightRouteModel.origin_airport_iata == origin_iata_code)
            .distinct()
            .all()
        )

        destination_iata_codes = [item[0] for item in destination_iatas]

        if not destination_iata_codes:
            return []

        airports_db = (
            db.query(AirportModel)
            .filter(AirportModel.iata_code.in_(destination_iata_codes))
            .order_by(AirportModel.iata_code)
            .all()
        )

        airports = [Airport.from_orm(airport) for airport in airports_db]

        return airports

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des destinations: {str(e)}") from e
