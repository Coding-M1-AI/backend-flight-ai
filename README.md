# Flight Delay Prediction API

API simplifiée pour la prédiction des retards de vol avec **Ray** et **FastAPI**.

## Architecture du Projet

```
backend-ia/                           # API Backend avec Ray + PostgreSQL
├── app/
│   ├── __init__.py                   # Application FastAPI principale
│   ├── config.py                     # Configuration (Settings)
│   ├── database.py                   # Configuration SQLAlchemy
│   ├── models.py                     # Modèles SQLAlchemy
│   ├── routes/
│   │   ├── __init__.py               # Router principal combiné
│   │   ├── health.py                 # Healthcheck + status Ray
│   │   ├── ml.py                     # ML (fit/predict)
│   │   └── data.py                   # Données (airlines/airports)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── data.py                   # Schémas Pydantic (data)
│   │   └── ml.py                     # Schémas Pydantic (ML)
│   └── services/
│       ├── __init__.py
│       ├── data_service.py           # Service traitement données avec Ray Data
│       └── ray_service.py            # Orchestration Ray (acteur modèle)
├── data/
│   ├── airlines.csv                  # 15 compagnies aériennes
│   ├── airports.csv                  # 300+ aéroports US
│   └── flights.csv                   # Données de vols
├── models/                           # Modèles ML (.pkl) - vide par défaut
├── scripts/
│   ├── import_model.py               # Import depuis ai-models
│   ├── import_csv_to_db.py           # CSV → PostgreSQL
│   └── setup_database.py             # Setup complet DB
├── docker-compose.yml                # Configuration Docker Compose
├── Dockerfile                        # Image Docker de l'API
├── main.py                           # Point d'entrée uvicorn
├── pyproject.toml                    # Configuration uv/pip
├── requirements.txt                  # Dépendances Python
└── README.md                         
```

## Quick Start

### Option 1: Avec Docker Compose (Recommandé)

```bash
cd backend-ia
docker-compose up --build
```

Cela lancera automatiquement :
- PostgreSQL (port 5432)
- L'API FastAPI (port 8000)
- Setup de la base de données et import des données

L'API sera disponible sur http://localhost:8000

### Option 2: Installation Manuelle

#### 1. Installation des dépendances
```bash
cd backend-ia
uv pip install -r requirements.txt
# ou avec uv directement
uv pip install -e .
```

#### 2. Setup PostgreSQL
```bash
# Avec Docker (recommandé)
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=flightdb \
  -p 5432:5432 postgres:15-alpine

# Ou utiliser docker-compose uniquement pour la DB
docker-compose up db -d
```

#### 3. Setup Base de Données + Import Données
```bash
# Configuration complète : tables + import CSV
python scripts/setup_database.py
```

#### 4. Importer le modèle ML
```bash
# Copie le modèle depuis ai-models/main.ipynb
python scripts/import_model.py
```

#### 5. Lancer l'API
```bash
python main.py
```

L'API sera disponible sur http://localhost:8000

## 5 Endpoints Principaux

| Endpoint | Méthode | Description | 
|----------|---------|-------------|
| `/api/v1/fit` | **POST** | Entraîner le modèle avec Ray |
| `/api/v1/predict` | **POST** | Prédiction de retard avec Ray |
| `/api/v1/health` | **GET** | Healthcheck + status Ray |
| `/api/v1/airlines` | **GET** | Liste des compagnies (CSV) |
| `/api/v1/airports` | **GET** | Liste des aéroports (CSV) |

### Exemple d'utilisation

**Prédiction de retard:**
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
-H "Content-Type: application/json" \
-d '{"month": 6}'
```

**Réponse:**
```json
{
  "month": 6,
  "predicted_delay": 25.3,
  "model_version": "v1.0"
}
```

**Healthcheck:**
```bash
curl http://localhost:8000/api/v1/health
```

**Compagnies aériennes:**
```bash
curl http://localhost:8000/api/v1/airlines
```

## Modèle ML

| Aspect | Détail |
|--------|---------|
| **Type** | RandomForest Regressor |
| **Entraînement** | `ai-models/main.ipynb` |
| **Features** | MONTH, DAY, AIRLINE, AIRPORTS, DEPARTURE_DELAY |
| **Performance** | R² 92% (train) / 46% (test) |
| **Données** | 10k échantillons de vols US 2015 |
| **Orchestration** | Ray pour distribution |

## Ray Orchestration

- **Acteur persistant** maintient le modèle en mémoire
- **Prédictions distribuées** via `model.predict.remote()`
- **Scalabilité horizontale** automatique  
- **Performance optimisée** pour la production

## Données Incluses

| Dataset | Contenu | Source |
|---------|---------|--------|
| **Airlines** | 15 compagnies (UA, AA, DL...) | `data/airlines.csv` |
| **Airports** | 300+ aéroports US + GPS | `data/airports.csv` | 
| **Modèle** | RandomForest entraîné | `ai-models/main.ipynb` |

## Workflow ML

```mermaid
graph LR
    A[ai-models/main.ipynb] --> B[Entraînement]
    B --> C[Modèle .pkl]
    C --> D[scripts/import_model.py]
    D --> E[backend-ia/models/]
    E --> F[Ray Service]
    F --> G[API /predict]
```

1. **Développement ML** dans `ai-models/main.ipynb` 
2. **Export modèle** vers `backend-ia/models/`
3. **Déploiement API** avec Ray orchestration
4. **Prédictions** via endpoints REST

## Documentation

- **Swagger UI:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc

## Technologies Utilisées

- **FastAPI** : Framework web moderne et rapide
- **Ray** : Orchestration distribuée pour ML
- **PostgreSQL** : Base de données relationnelle
- **SQLAlchemy** : ORM Python
- **Pydantic** : Validation des données
- **uv** : Gestionnaire de paquets rapide
- **Docker** : Conteneurisation
