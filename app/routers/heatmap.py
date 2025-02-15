# app/routes.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db  # Importation de la session de base de données
from app import templates
from app.services import obtenir_donnees_heatmap  # Importation de la fonction service

router = APIRouter()

@router.get("/obtenir_donnees_heatmap")
def obtenir_donnees_heatmap_route(db: Session = Depends(get_db)):
    """
    Fonction pour obtenir les données de la heatmap :
    - Récupère les zones et les infrastructures.
    - Calcule le score pour chaque zone en fonction des distances aux infrastructures.
    """
    try:
        donnees = obtenir_donnees_heatmap(db)
        return donnees
    except Exception as e:
        return {"erreur": str(e)}  # Retourne l'erreur si problème

@router.get("", response_class=HTMLResponse)
async def afficher_page_heatmap(request: Request):
    """
    Affiche la page HTML avec la carte et la heatmap
    """
    return templates.TemplateResponse("heatmap.html", {"request": request})
