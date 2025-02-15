from sqlalchemy.orm import Session
from sqlalchemy import text

def get_zone_coordinates(db: Session):
    """
    Récupère les coordonnées des zones depuis la base de données.
    """
    try:
        # Exécution de la requête pour récupérer les données des zones
        zones = db.execute(
            text("""
                SELECT id_zone, latitude_centre, longitude_centre,
                       latitude_min, longitude_min, latitude_max, longitude_max
                FROM angers_cadrillage
            """)
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
        raise Exception(f"Erreur lors de la récupération des coordonnées des zones : {str(e)}")
