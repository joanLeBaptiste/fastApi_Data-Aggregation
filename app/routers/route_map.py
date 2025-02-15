from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import get_zone_coordinates
from app import templates

router = APIRouter()

@router.get("/obtenir_coordonnees_zones")
def obtenir_coordonnees_zones_route(db: Session = Depends(get_db)):
    """
    Endpoint pour obtenir les coordonnées des zones.
    """
    try:
        zones = get_zone_coordinates(db)
        return zones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_class=HTMLResponse)
async def afficher_page_carte_zones(request: Request):
    """
    Affiche la carte des zones avec les centres et délimitations
    """
    return templates.TemplateResponse("cadrillage.html", {"request": request})
