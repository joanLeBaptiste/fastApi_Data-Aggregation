from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db

from app import templates

router = APIRouter()

# Route pour obtenir les coordonnées des zones
@router.get("/obtenir_coordonnees_zones")
def obtenir_coordonnees_zones(db: Session = Depends(get_db)):
    """
    Récupère les coordonnées des zones depuis la base de données
    """
    try:
        # Remplace l'exécution directe de la requête SQL par l'utilisation de la session SQLAlchemy
        zones = db.execute(
            """
            SELECT id_zone, latitude_centre, longitude_centre,
                   latitude_min, longitude_min, latitude_max, longitude_max
            FROM angers_cadrillage
            """
        ).fetchall()

        zones_json = [
            {
                "id": zone[0],
                "latitude_centre": zone[1],
                "longitude_centre": zone[2],
                "latitude_min": zone[3],
                "longitude_min": zone[4],
                "latitude_max": zone[5],
                "longitude_max": zone[6],
            }
            for zone in zones
        ]
        return zones_json
    except Exception as e:
        return {"erreur": str(e)}  # Retourne l'erreur si problème


# Route HTML pour afficher la carte
@router.get("", response_class=HTMLResponse)
async def afficher_page_carte_zones(request: Request):
    """
    Affiche une carte d'Angers avec les centres des zones en rouge et leurs délimitations (carré bleu)
    """
    return templates.TemplateResponse("cadrillage.html", {"request": request})
