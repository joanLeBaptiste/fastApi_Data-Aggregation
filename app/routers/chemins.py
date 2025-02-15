from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app import templates
import json

from app.services import (
    obtenir_couleur_centre,
    obtenir_infrastructures_par_chemins,
    obtenir_zones_pour_heatmap,
    couleurs_infrastructures
)

router = APIRouter()

@router.get("/get_center_color/{id_zone}")
def obtenir_couleur_centre_route(id_zone: str, db: Session = Depends(get_db)):
    """
    Route pour obtenir la couleur d'une zone en fonction de la distance moyenne.
    """
    try:
        result = obtenir_couleur_centre(db, id_zone)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@router.get("/get_infrastructure_by_paths/{id_zone}")
def obtenir_infrastructures_par_chemins_route(id_zone: str, db: Session = Depends(get_db)):
    """
    Route pour obtenir les infrastructures associées aux chemins d'une zone donnée.
    """
    try:
        result = obtenir_infrastructures_par_chemins(db, id_zone)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")

@router.get("", response_class=JSONResponse)
def page_heatmap(request: Request, db: Session = Depends(get_db)):
    """
    Route pour afficher la carte interactive en envoyant les données nécessaires au template.
    """
    try:
        zones_list = obtenir_zones_pour_heatmap(db)
        return templates.TemplateResponse("chemins.html", {
            "request": request,
            "zones_list": json.dumps(zones_list),
            "couleurs_infrastructures": json.dumps(couleurs_infrastructures)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur: {str(e)}")