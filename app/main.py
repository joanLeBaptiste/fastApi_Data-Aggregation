from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import des routeurs centralisés dans __init__.py du package routeur
from app.routers import (
    chemins_router,
    heatmap_router,
    super_heatmap_router,
    zones_scores_router,
    route_test_router,
    route_map_router,
)

# Import des éléments centralisés dans app/__init__.py
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

# Initialisation de l'application
app = FastAPI()

# Inclusion des routeurs
app.include_router(route_test_router, prefix="/test", tags=["Test"])
app.include_router(zones_scores_router, prefix="/zones", tags=["Zones"])
app.include_router(route_map_router, prefix="/map", tags=["Map"])
app.include_router(heatmap_router, prefix="/heatmap", tags=["Heatmap"])
app.include_router(super_heatmap_router, prefix="/superheatmap", tags=["SuperHeatmap"])
app.include_router(chemins_router, prefix="/chemins", tags=["Chemins"])

# Ajout des fichiers statiques
app.mount("/asset", StaticFiles(directory="./app/asset"), name="asset")


# Routes pour tester la base de données
@app.get("/test_db", tags=["Test"])
def test_db(db: Session = Depends(get_db)):  # Utilisation propre de get_db()
    try:
        res = db.execute("SELECT 1").scalar()
        return {"message": "Database connection successful", "result": res}
    except Exception as e:
        return {"error": str(e)}


# Page de base
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "test allo"}


# Événement pour lister les routes disponibles
@app.on_event("startup")
async def list_routes():
    print("📋 Routes disponibles :")
    for route in app.routes:
        print(f"{route.path} -> {route.name}")


# uvicorn app.main:app --reload
