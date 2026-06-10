from fastapi import APIRouter, Depends
from core import get_db, get_dw
from controllers import DimFechaController
from models import Fecha

router = APIRouter(prefix="/scheduled", tags=["Scheluded"])

def fecha_controller(dw = Depends(get_dw)):
    return DimFechaController(dw)

@router.post("/fechas_mensuales")
def crear_fechas_mensuales(request: Fecha, controller: DimFechaController = Depends(fecha_controller)):
    return controller.crear_fechas_mensuales(request.fecha)
