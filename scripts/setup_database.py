#!/usr/bin/env python3
"""
Script de configuration complète de la base de données

Usage:
    python scripts/setup_database.py

Ce script fait tout en une seule commande :
1. Vérifie la connexion à PostgreSQL
2. Crée les tables si nécessaire
3. Importe les données CSV
4. Vérifie que tout fonctionne

Pour un démarrage rapide !
"""

import sys
import time
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.import_csv_to_db import main as import_csv_main
from sqlalchemy import text

from app.database import Base, engine
from app.models import Airline, Airport, FlightRoute


def check_database_connection():
    """Vérifier la connexion à la base de données"""
    print("Vérification de la connexion à la base de données...")

    try:
        # Tentative de connexion simple
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()

        print("Connexion à PostgreSQL réussie")
        return True

    except Exception as e:
        print(f"Impossible de se connecter à la base de données: {e}")
        print("\nConseil: Vérifiez que PostgreSQL est démarré:")
        print("   docker run -d --name postgres \\")
        print("     -e POSTGRES_PASSWORD=postgres \\")
        print("     -e POSTGRES_DB=flightdb \\")
        print("     -p 5432:5432 postgres:15-alpine")
        print("\n   Ou démarrez avec docker-compose:")
        print("   docker-compose up -d")
        return False


def create_tables():
    """Créer toutes les tables"""
    print("\nCréation des tables...")

    try:
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès")

        # Lister les tables créées
        tables = ["flight_data", "prediction_results", "airlines", "airports", "flight_routes"]

        print("Tables disponibles:")
        for table in tables:
            print(f"   - {table}")

        return True

    except Exception as e:
        print(f"Erreur lors de la création des tables: {e}")
        return False


def verify_data():
    """Vérifier que les données ont été importées"""
    print("\nVérification des données importées...")

    try:
        from sqlalchemy.orm import sessionmaker

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        # Compter les enregistrements
        airlines_count = session.query(Airline).count()
        airports_count = session.query(Airport).count()

        session.close()

        print(f"Compagnies aériennes: {airlines_count}")
        print(f"Aéroports: {airports_count}")

        if airlines_count > 0 and airports_count > 0:
            print("Données importées avec succès!")
            return True
        else:
            print("Attention: certaines tables sont vides")
            return False

    except Exception as e:
        print(f"Erreur lors de la vérification: {e}")
        return False


def main():
    """Fonction principale de configuration"""
    print("Configuration complète de la base de données")
    print("=" * 60)

    # Étape 1: Vérifier la connexion
    if not check_database_connection():
        print("\nArrêt du script - base de données non accessible")
        sys.exit(1)

    # Petit délai pour laisser la DB se stabiliser
    time.sleep(1)

    # Étape 2: Créer les tables
    if not create_tables():
        print("\nArrêt du script - erreur lors de la création des tables")
        sys.exit(1)

    # Étape 3: Importer les données CSV
    print("\n" + "=" * 60)
    print("Import des données CSV...")

    try:
        import_csv_main()
    except SystemExit:
        # Le script d'import peut faire sys.exit(1) en cas d'erreur
        print("\nErreur lors de l'import des données")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue lors de l'import: {e}")
        sys.exit(1)

    # Étape 4: Vérification finale
    print("\n" + "=" * 60)
    if verify_data():
        print("\nConfiguration terminée avec succès!")
        print("Votre base de données est prête.")
        print("Vous pouvez maintenant démarrer l'API:")
        print("   python main.py")
        print("\nEndpoints disponibles:")
        print("   • POST /api/v1/fit")
        print("   • POST /api/v1/predict")
        print("   • GET  /api/v1/health")
        print("   • GET  /api/v1/airlines")
        print("   • GET  /api/v1/airports")
    else:
        print("\nConfiguration partiellement réussie")
        print("Certaines fonctionnalités peuvent ne pas fonctionner")
        sys.exit(1)


if __name__ == "__main__":
    main()
