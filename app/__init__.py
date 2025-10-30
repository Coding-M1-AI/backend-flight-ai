from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes import main_router

# Créer les tables de la base de données
try:
    Base.metadata.create_all(bind=engine)
    print("Tables de la base de données créées/vérifiées")
except Exception as e:
    print(f"Attention: Problème avec la base de données: {e}")
    quit()

app = FastAPI(
    title="Flight Delay Prediction API",
    description="API simplifiée pour la prédiction des retards de vol avec Ray + PostgreSQL",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes principales
app.include_router(main_router, prefix="/api/v1")
