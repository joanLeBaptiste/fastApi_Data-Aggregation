from fastapi import APIRouter, Request, Depends
from sqlalchemy import text
import math
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db  # Importation de la session de base de données
from app import templates

router = APIRouter()

# Fonction pour calculer la distance entre deux coordonnées
def haversine(lat1, lon1, lat2, lon2):
    """
    Calcule la distance entre deux points géographiques en kilomètres.
    """
    R = 6371  # Rayon moyen de la Terre (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Route pour calculer le score des zones
@router.get("/calculer_scores_zones")
def calculer_scores_zones(db: Session = Depends(get_db)):
    """
    Calcule le score total reçu par chaque zone en fonction des distances aux infrastructures.
    """
    try:
        # Récupérer les zones
        zones = db.execute(
            text("SELECT id_zone, latitude_centre, longitude_centre, rayon_km FROM angers_cadrillage")
        ).fetchall()

        # Récupérer les infrastructures avec leurs scores
        infrastructures = db.execute(text(""" 
            SELECT I.latitude, I.longitude, T.score
            FROM infrastructures I
            JOIN type_scores T ON I.type_infra = T.type_infra
        """)).fetchall()

        scores_zones = []
        for zone in zones:
            zone_id, zone_lat, zone_lon, zone_radius = zone
            total_score = 0

            # Calcul du score total en fonction des infrastructures
            for infra in infrastructures:
                infra_lat, infra_lon, infra_score = infra
                distance = haversine(zone_lat, zone_lon, infra_lat, infra_lon)

                # Si l'infrastructure est dans le rayon de la zone, score plein
                if distance <= zone_radius:
                    total_score += infra_score
                else:
                    # Contribution dégressive en fonction de la distance
                    total_score += infra_score * max(0, 1 - (distance - zone_radius) / (3 * zone_radius))

            scores_zones.append({"id_zone": zone_id, "score": total_score})

        return JSONResponse(content=scores_zones)

    except Exception as e:
        return JSONResponse(content={"erreur": str(e)}, status_code=500)


# Route HTML pour afficher les scores des zones
@router.get("", response_class=HTMLResponse)
async def page_scores_zones(request: Request):
    """
    Affiche une page HTML avec les graphiques des scores des zones.
    """
    return templates.TemplateResponse("zones_scores.html", {"request": request})
