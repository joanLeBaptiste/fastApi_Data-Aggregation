from fastapi import APIRouter, Request, Depends
from sqlalchemy import text
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db  # Importation de la session de base de données
from app import templates

router = APIRouter()


@router.get("/get_type_scores")
def get_type_scores(db: Session = Depends(get_db)):
    """
    Récupère les types d'infrastructures et leurs scores associés depuis la base de données.
    """
    try:
        requete = text("SELECT type_infra, score FROM type_scores")
        result = db.execute(requete).fetchall()

        # Conversion en JSON
        donnee = [{"type_infra": row[0], "score": row[1]} for row in result]

        return JSONResponse(content=donnee)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("", response_class=HTMLResponse)
def type_scores_page(request: Request):
    """
    Route pour afficher une page HTML de test.
    """
    return templates.TemplateResponse("route_test.html", {"request": request})
