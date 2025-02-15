from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import get_all_type_scores
from app import templates

router = APIRouter()

@router.get("/get_type_scores")
def get_type_scores_route(db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer les types d'infrastructures et leurs scores.
    """
    try:
        data = get_all_type_scores(db)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_class=HTMLResponse)
def type_scores_page(request: Request):
    """
    Affiche une page HTML de test.
    """
    return templates.TemplateResponse("route_test.html", {"request": request})
