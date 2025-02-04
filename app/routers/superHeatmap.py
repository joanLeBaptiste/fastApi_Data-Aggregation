from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db  # Importation de la session de base de données
from app import templates
from fastapi.responses import HTMLResponse

import math
from sqlalchemy import text

router = APIRouter()


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@router.get("/get_heatmap_data2")
def get_heatmap_data2(db: Session = Depends(get_db)):
    """
    Calcule les distances moyennes aux infrastructures pour chaque zone.
    """
    try:
        # Récupérer les zones
        zones = db.execute(
            text("""
            SELECT id_zone, latitude_centre, longitude_centre,
                   latitude_min, longitude_min,
                   latitude_max, longitude_max
            FROM angers_cadrillage
            """)
        ).fetchall()

        # Récupérer les infrastructures
        infrastructures = db.execute(
            text("""
            SELECT latitude, longitude FROM infrastructures
            """)
        ).fetchall()

        heatmap_donnee = []
        for zone in zones:
            id_zone, lat_centre, lon_centre, lat_min, lon_min, lat_max, lon_max = zone
            distances = []

            # Calculer les distances moyennes pour la zone
            for infra in infrastructures:
                infra_lat, infra_lon = infra
                distances.append(haversine(lat_centre, lon_centre, infra_lat, infra_lon))

            avg_distance = sum(distances) / len(distances) if distances else 0

            # Ajouter les données pour la heatmap
            heatmap_donnee.append({
                "id": id_zone,
                "latitude_min": lat_min,
                "longitude_min": lon_min,
                "latitude_max": lat_max,
                "longitude_max": lon_max,
                "distance_moyenne": avg_distance
            })

        return heatmap_donnee
    except Exception as e:
        return {"error": str(e)}


@router.get("/get_infrastructure_data")
def get_infrastructure_data(db: Session = Depends(get_db)):
    """
    Récupère les données des infrastructures avec leur type.
    """
    try:
        infrastructures = db.execute(
            text("""
            SELECT nom, type_infra, latitude, longitude
            FROM infrastructures
            """)
        ).fetchall()

        infra_donnee = [
            {"name": infra[0], "type": infra[1], "latitude": infra[2], "longitude": infra[3]}
            for infra in infrastructures
        ]

        return infra_donnee
    except Exception as e:
        return {"error": str(e)}


@router.get("", response_class=HTMLResponse)
async def heatmap_zones_page(request: Request):
    """
    Affiche une carte interactive avec une heatmap et des points pour les infrastructures
    """
    return templates.TemplateResponse("heatmap2.html", {"request": request})
