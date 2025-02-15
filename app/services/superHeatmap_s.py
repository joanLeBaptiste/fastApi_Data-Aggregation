from sqlalchemy.orm import Session
from app.utils.haversine import haversine
from app.models import AngersCadrillage, Infrastructures


def get_heatmap_data(db: Session):
    """
    Calcule la distance moyenne des infrastructures pour chaque zone.
    """
    try:
        # Récupération des zones
        zones = db.query(
            AngersCadrillage.id_zone,
            AngersCadrillage.latitude_centre,
            AngersCadrillage.longitude_centre,
            AngersCadrillage.latitude_min,
            AngersCadrillage.longitude_min,
            AngersCadrillage.latitude_max,
            AngersCadrillage.longitude_max
        ).all()

        # Récupération des infrastructures
        infrastructures = db.query(
            Infrastructures.latitude,
            Infrastructures.longitude
        ).all()

        heatmap_data = []
        for zone in zones:
            id_zone, lat_centre, lon_centre, lat_min, lon_min, lat_max, lon_max = zone
            distances = [haversine(lat_centre, lon_centre, infra_lat, infra_lon) for infra_lat, infra_lon in infrastructures]

            avg_distance = sum(distances) / len(distances) if distances else 0

            heatmap_data.append({
                "id": id_zone,
                "latitude_min": lat_min,
                "longitude_min": lon_min,
                "latitude_max": lat_max,
                "longitude_max": lon_max,
                "distance_moyenne": avg_distance
            })

        return heatmap_data

    except Exception as e:
        raise RuntimeError(f"Erreur lors du calcul des distances moyennes : {str(e)}")


def get_infrastructure_data(db: Session):
    """
    Récupère les infrastructures et leurs types.
    """
    try:
        infrastructures = db.query(
            Infrastructures.nom,
            Infrastructures.type_infra,
            Infrastructures.latitude,
            Infrastructures.longitude
        ).all()

        return [
            {"name": nom, "type": type_infra, "latitude": lat, "longitude": lon}
            for nom, type_infra, lat, lon in infrastructures
        ]

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la récupération des infrastructures : {str(e)}")
