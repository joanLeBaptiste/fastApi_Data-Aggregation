from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse

from app.database import get_db
from app.services import calculer_scores_zones
from app import templates

router = APIRouter()


@router.get("/calculer_scores_zones")
def get_scores_zones(db: Session = Depends(get_db)):
    """
    API pour récupérer les scores des zones en fonction des infrastructures.
    """
    try:
        scores_zones = calculer_scores_zones(db)
        return JSONResponse(content=scores_zones)
    except RuntimeError as e:
        return JSONResponse(content={"erreur": str(e)}, status_code=500)


@router.get("", response_class=HTMLResponse)
async def page_scores_zones(request: Request):
    """
    Affiche une page HTML avec les scores des zones sous forme graphique.
    """
    return templates.TemplateResponse("zones_scores.html", {"request": request})
