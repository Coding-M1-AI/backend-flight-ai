#!/usr/bin/env python3
"""
Script pour importer les données CSV vers la base de données

Usage:
    python scripts/import_csv_to_db.py

Le script importe airlines.csv et airports.csv vers PostgreSQL
"""

import csv
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import Airline, Airport


def import_airlines(session, csv_file_path: str):
    """Importer les données des compagnies aériennes"""

    if not os.path.exists(csv_file_path):

        print(f"Fichier {csv_file_path} non trouvé")
        return False

    print(f"Import des compagnies aériennes depuis {csv_file_path}")

    # Vider la table existante
    session.query(Airline).delete()
    session.commit()

    imported_count = 0

    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            airlines_to_add = []

            for row in reader:
                # Ignorer les lignes vides
                if row.get("IATA_CODE") and row.get("AIRLINE"):
                    airline = Airline(iata_code=row["IATA_CODE"].strip(), airline_name=row["AIRLINE"].strip())
                    airlines_to_add.append(airline)
                    imported_count += 1

            # Insertion en lot pour optimiser les performances
            if airlines_to_add:
                session.add_all(airlines_to_add)
                session.commit()

        print(f"{imported_count} compagnies aériennes importées")
        return True

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'import des airlines: {e}")
        return False


def import_airports(session, csv_file_path: str):
    """Importer les données des aéroports"""

    if not os.path.exists(csv_file_path):
        print(f"Fichier {csv_file_path} non trouvé")
        return False

    print(f"Import des aéroports depuis {csv_file_path}")

    # Vider la table existante
    session.query(Airport).delete()
    session.commit()

    imported_count = 0

    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            airports_to_add = []

            for row in reader:
                # Ignorer les lignes vides
                if row.get("IATA_CODE") and row.get("AIRPORT"):
                    # Conversion sécurisée des coordonnées
                    latitude = None
                    longitude = None

                    try:
                        if row.get("LATITUDE"):
                            latitude = float(row["LATITUDE"])
                    except (ValueError, TypeError):
                        latitude = None

                    try:
                        if row.get("LONGITUDE"):
                            longitude = float(row["LONGITUDE"])
                    except (ValueError, TypeError):
                        longitude = None

                    airport = Airport(
                        iata_code=row["IATA_CODE"].strip(),
                        airport_name=row["AIRPORT"].strip(),
                        city=row.get("CITY", "").strip() or None,
                        state=row.get("STATE", "").strip() or None,
                        country=row.get("COUNTRY", "").strip() or None,
                        latitude=latitude,
                        longitude=longitude,
                    )
                    airports_to_add.append(airport)
                    imported_count += 1

            # Insertion en lot pour optimiser les performances
            if airports_to_add:
                session.add_all(airports_to_add)
                session.commit()

        print(f"{imported_count} aéroports importés")
        return True

    except Exception as e:
        session.rollback()
        print(f"Erreur lors de l'import des airports: {e}")
        return False


def main():
    print("Import des données CSV vers la base de données...")
    print("=" * 60)

    try:
        # Créer la session de base de données
        session = SessionLocal()

        # Chemins vers les fichiers CSV
        airlines_csv = "data/airlines.csv"
        airports_csv = "data/airports.csv"

        success = True

        # Import des compagnies aériennes
        if not import_airlines(session, airlines_csv):
            success = False

        # Import des aéroports
        if not import_airports(session, airports_csv):
            success = False

        # Fermer la session
        session.close()

        print()
        if success:
            print("Import terminé avec succès !")
        else:
            print("Échec de l'import")
            print("Vérifiez la configuration de la base de données")
            sys.exit(1)

    except Exception as e:
        print(f"Erreur critique: {e}")
        print("Vérifiez que la base de données PostgreSQL est démarrée")
        sys.exit(1)


if __name__ == "__main__":
    main()
