from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse

from app.database import get_db
from app.services import get_heatmap_data, get_infrastructure_data
from app import templates

router = APIRouter()


@router.get("/get_heatmap_data2")
def get_heatmap_data_route(db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer les données de la heatmap (distance moyenne aux infrastructures par zone).
    """
    try:
        data = get_heatmap_data(db)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_infrastructure_data")
def get_infrastructure_data_route(db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer les infrastructures et leurs types.
    """
    try:
        data = get_infrastructure_data(db)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_class=HTMLResponse)
async def heatmap_zones_page(request: Request):
    """
    Affiche une carte interactive avec la heatmap et les infrastructures.
    """
    return templates.TemplateResponse("heatmap2.html", {"request": request})
