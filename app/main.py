from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


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
@app.get("/", tags=["Root"], response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
        <head>
            <title>Accès aux Pages</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    color: #333;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    text-align: center;
                }
                h1 {
                    padding: 20px;
                    background-color: #4CAF50;
                    color: white;
                    margin: 0;
                    font-size: 24px;
                }
                .container {
                    padding: 20px;
                    max-width: 600px;
                    width: 100%;
                    box-sizing: border-box;
                }
                h2 {
                    font-size: 20px;
                    margin-bottom: 20px;
                }
                .links {
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .links li {
                    margin: 0;
                }
                .links a {
                    color: #4CAF50;
                    text-decoration: none;
                    padding: 12px;
                    border: 2px solid #4CAF50;
                    border-radius: 5px;
                    font-size: 18px;
                    transition: background-color 0.3s, color 0.3s;
                    display: inline-block;
                    width: 100%;
                    text-align: center;
                }
                .links a:hover {
                    background-color: #4CAF50;
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Bienvenue sur le Projet d'agregation de données</h1>
                <h2>Accéder aux pages disponibles:</h2>
                <ul class="links">
                    <li><a href="http://127.0.0.1:8000/heatmap">Heatmap densité infrastructures</a></li>
                    <li><a href="http://127.0.0.1:8000/superheatmap">Heatmap distances aux infrastructures</a></li>
                    <li><a href="http://127.0.0.1:8000/chemins">Affichage des centres zones avec chemins</a></li>
                    <li><a href="http://127.0.0.1:8000/map">Carte des zones</a></li>
                    <li><a href="http://127.0.0.1:8000/zones">Scores des zones, graphique</a></li>
                    <li><a href="http://127.0.0.1:8000/test">Score attribué aux infrastructures</a></li>
                </ul>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# l
# Événement pour lister les routes disponibles
@app.on_event("startup")
async def list_routes():
    print("📋 Routes disponibles :")
    for route in app.routes:
        print(f"{route.path} -> {route.name}")


# uvicorn app.main:app --reload
