from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from app.database import get_db  # Importation de la session de base de données
from app import templates
import math
from sqlalchemy import text


router = APIRouter()


# ✅ Fonction Haversine pour calculer la distance entre deux points
def haversine(latitude1, longitude1, latitude2, longitude2):
    RAYON_TERRRE = 6371  # Rayon de la Terre en km
    delta_latitude = math.radians(latitude2 - latitude1)
    delta_longitude = math.radians(longitude2 - longitude1)
    a = math.sin(delta_latitude / 2) ** 2 + math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * math.sin(delta_longitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return RAYON_TERRRE * c  # Retourne la distance en km


@router.get("/obtenir_donnees_heatmap")
def obtenir_donnees_heatmap(db: Session = Depends(get_db)):
    """
    Fonction pour obtenir les données de la heatmap :
    - Récupère les zones et les infrastructures.
    - Calcule le score pour chaque zone en fonction des distances aux infrastructures.
    """
    try:
        # Récupération des zones
        zones = db.execute(
            text("""
            SELECT id_zone, latitude_centre, longitude_centre,
                   latitude_min, longitude_min, latitude_max, longitude_max, rayon_km
            FROM angers_cadrillage
            """)
        ).fetchall()

        # Récupération des infrastructures avec leurs scores et types
        infrastructures = db.execute(
            text("""
            SELECT I.latitude, I.longitude, T.score, I.type_infra
            FROM infrastructures I
            JOIN type_scores T ON I.type_infra = T.type_infra
            """)
        ).fetchall()

        donnees_heatmap = []
        for zone in zones:
            (id_zone, lat_centre, lon_centre,
             lat_min, lon_min, lat_max, lon_max, rayon_km) = zone

            score_total = 0
            infra_par_type = {}

            # Calcul des scores et comptage des types d'infrastructures
            for infra in infrastructures:
                infra_lat, infra_lon, infra_score, infra_type = infra
                distance = haversine(lat_centre, lon_centre, infra_lat, infra_lon)

                if distance <= rayon_km:
                    score_total += infra_score
                    infra_par_type[infra_type] = infra_par_type.get(infra_type, 0) + 1
                else:
                    score_total += infra_score * max(0, 1 - (distance - rayon_km) / (3 * rayon_km))

            donnees_heatmap.append({
                "id": id_zone,
                "latitude_min": lat_min,
                "longitude_min": lon_min,
                "latitude_max": lat_max,
                "longitude_max": lon_max,
                "score": score_total,
                "infrastructures": infra_par_type
            })

        return donnees_heatmap
    except Exception as e:
        return {"erreur": str(e)}  # Retourne l'erreur si problème


@router.get("", response_class=HTMLResponse)
async def afficher_page_heatmap(request: Request):
    """
    Affiche la page HTML avec la carte et la heatmap
    """
    return templates.TemplateResponse("heatmap.html", {"request": request})
