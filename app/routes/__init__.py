"""
Routes de l'API - Organisation modulaire

Structure:
- health.py : Healthcheck et status
- ml.py     : Machine Learning (fit/predict)
- data.py   : Données (airlines/airports)
"""

from fastapi import APIRouter

from . import data, health, ml

# Router principal qui combine tous les sous-routers
main_router = APIRouter()

# Inclure tous les sous-routers
main_router.include_router(health.router, tags=["health"])
main_router.include_router(ml.router, tags=["machine-learning"])
main_router.include_router(data.router, tags=["data"])

# Export pour faciliter l'import depuis app/__init__.py
__all__ = ["main_router", "health", "ml", "data"]
