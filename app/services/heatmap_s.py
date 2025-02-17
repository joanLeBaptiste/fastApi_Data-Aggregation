from sqlalchemy.orm import Session
from app.models import AngersCadrillage  # Seulement le modèle pour les zones (première requête)
from sqlalchemy import text
from app.utils.haversine import haversine  # Utilisation d'un utilitaire externe pour le calcul


# ✅ Récupérer les données nécessaires pour la heatmap
def obtenir_donnees_heatmap(db: Session):
    try:
        # Récupération des zones via le modèle SQLAlchemy
        zones = db.query(AngersCadrillage).all()

        # Récupération des infrastructures et de leurs scores à partir de la vue
        infrastructures = db.execute(text("""
            SELECT infra_latitude, infra_longitude, score, type_infra
            FROM vue_infrastructures_scores
        """)).fetchall()

        donnees_heatmap = []
        for zone in zones:
            lat_centre, lon_centre = zone.latitude_centre, zone.longitude_centre
            lat_min, lon_min, lat_max, lon_max, rayon_km = zone.latitude_min, zone.longitude_min, zone.latitude_max, zone.longitude_max, zone.rayon_km

            score_total = 0
            infra_par_type = {}

            # Calcul des scores et comptage des types d'infrastructures
            for infra_lat, infra_lon, infra_score, infra_type in infrastructures:
                distance = haversine(lat_centre, lon_centre, infra_lat, infra_lon)

                if distance <= rayon_km:
                    score_total += infra_score
                    infra_par_type[infra_type] = infra_par_type.get(infra_type, 0) + 1
                else:
                    score_total += infra_score * max(0, 1 - (distance - rayon_km) / (3 * rayon_km))

            donnees_heatmap.append({
                "id": zone.id_zone,
                "latitude_min": lat_min,
                "longitude_min": lon_min,
                "latitude_max": lat_max,
                "longitude_max": lon_max,
                "score": score_total,
                "infrastructures": infra_par_type
            })

        return donnees_heatmap
    except Exception as e:
        raise Exception(f"Erreur lors de l'obtention des données de la heatmap : {e}")
