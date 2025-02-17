from sqlalchemy.orm import Session
from app.utils.haversine import haversine  # Utilisation d'un utilitaire externe pour le calcul
from app.models import AngersCadrillage  # Seulement le modèle pour la zone (première requête)
from sqlalchemy import text

def calculer_scores_zones(db: Session):
    """
    Calcule le score total pour chaque zone en fonction des distances aux infrastructures.
    """
    try:
        # Récupération des zones
        zones = db.query(
            AngersCadrillage.id_zone,
            AngersCadrillage.latitude_centre,
            AngersCadrillage.longitude_centre,
            AngersCadrillage.rayon_km
        ).all()

        # Récupération des infrastructures et de leurs scores à partir de la vue
        infrastructures = db.execute(text("""
            SELECT infra_latitude, infra_longitude, score, id_infra
            FROM vue_infrastructures_scores
        """)).fetchall()

        scores_zones = []
        for zone_id, zone_lat, zone_lon, zone_radius in zones:
            total_score = 0

            for infra_lat, infra_lon, infra_score, _ in infrastructures:
                distance = haversine(zone_lat, zone_lon, infra_lat, infra_lon)

                if distance <= zone_radius:
                    total_score += infra_score
                else:
                    total_score += infra_score * max(0, 1 - (distance - zone_radius) / (3 * zone_radius))

            scores_zones.append({"id_zone": zone_id, "score": total_score})

        return scores_zones

    except Exception as e:
        raise RuntimeError(f"Erreur lors du calcul des scores des zones : {str(e)}")
