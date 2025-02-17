from app.models import Chemin, AngersCadrillage
from sqlalchemy.orm import Session
from sqlalchemy import text


# Définition des couleurs pour chaque type d'infrastructure
couleurs_infrastructures = {
    "Médecin": "red",
    "Pharmacie": "green",
    "Pompiers": "blue",
    "Bibliothèque": "yellow",
    "Santé": "purple"
}

def obtenir_couleur_centre(db: Session, id_zone: str):
    """
    Récupère la couleur associée à une zone en fonction de la distance moyenne.
    """
    try:
        # Récupération de la distance moyenne des chemins pour la zone donnée
        chemins = db.query(Chemin).filter(Chemin.id_zone == id_zone).all()

        if not chemins:
            raise Exception("Aucune distance trouvée pour cette zone")

        # Calcul de la distance moyenne
        total_distance = sum(chemin.distance_m for chemin in chemins)
        avg_distance = total_distance / len(chemins) if chemins else 0

        avg_distance_km = avg_distance / 1000  # Conversion en km

        max_distance = 20  # Distance maximale en km
        if avg_distance_km > max_distance:
            color = 'red'
        else:
            normalized_distance = avg_distance_km / max_distance
            color = interpoler_couleur(normalized_distance)

        return {"id_zone": id_zone, "color": color}
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de la couleur : {str(e)}")

def interpoler_couleur(value):
    """
    Retourne une couleur RGB en fonction d'une valeur normalisée entre 0 et 1.
    Dégradé entre le vert (#00FF00) et le rouge (#FF0000).
    """
    red = int(255 * value)
    green = int(255 * (1 - value))
    return f"rgb({red}, {green}, 0)"

def obtenir_infrastructures_par_chemins(db: Session, id_zone: str):
    """
    Récupère les infrastructures associées aux chemins d'une zone donnée en utilisant la vue.
    """
    try:
        # Récupération des infrastructures via la vue 'vue_infrastructures_par_chemins'
        infrastructures = db.execute(text("""
            SELECT id_infra, nom, type_infra, latitude, longitude
            FROM vue_infrastructures_par_chemins
            WHERE id_zone = :id_zone
        """), {"id_zone": id_zone}).fetchall()

        if not infrastructures:
            raise Exception("Aucune infrastructure trouvée pour cette zone")

        result = [
            {
                "id_infra": infra.id_infra,
                "nom": infra.nom,
                "type_infra": infra.type_infra,
                "latitude": infra.latitude,
                "longitude": infra.longitude
            }
            for infra in infrastructures
        ]

        return result
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des infrastructures : {str(e)}")

def obtenir_zones_pour_heatmap(db: Session):
    """
    Récupère les zones depuis la base de données pour la heatmap.
    """
    try:
        # Récupération de toutes les zones
        zones = db.query(AngersCadrillage).all()

        result = [
            {
                "id_zone": zone.id_zone,
                "latitude_centre": zone.latitude_centre,
                "longitude_centre": zone.longitude_centre
            }
            for zone in zones
        ]

        return result
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des zones : {str(e)}")
