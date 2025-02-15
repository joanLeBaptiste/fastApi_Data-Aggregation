from sqlalchemy.orm import Session
from sqlalchemy import text

def get_all_type_scores(db: Session):
    """
    Récupère les types d'infrastructures et leurs scores associés depuis la base de données.
    """
    try:
        requete = text("SELECT type_infra, score FROM type_scores")
        result = db.execute(requete).fetchall()

        # Conversion en JSON
        donnee = [{"type_infra": row[0], "score": row[1]} for row in result]

        return donnee
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des données : {str(e)}")
