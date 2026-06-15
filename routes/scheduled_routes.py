from fastapi import APIRouter, Depends
from core import get_db, get_dw
from controllers import DimFechaController, HechosComprasController, HechosVentasController
from models import Fecha, RangoFechas

router = APIRouter(prefix="/scheduled", tags=["Scheluded"])

def fecha_controller(dw = Depends(get_dw)):
    return DimFechaController(dw)

def compras_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return HechosComprasController(db, dw)

def ventas_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return HechosVentasController(db,dw)

@router.post("/fechas_mensuales")
def crear_fechas_mensuales(request: Fecha, controller: DimFechaController = Depends(fecha_controller)):
    return controller.crear_fechas_mensuales(request.fecha)

@router.post("/compras_diarias")
def compras_diarias(fechas: RangoFechas, controller: HechosComprasController = Depends(compras_controller)):
    return controller.compras_etl(fechas)

@router.post("/insertar_venta")
def insertar_venta(fechas: RangoFechas, controller: HechosVentasController = Depends(ventas_controller)):
    return controller.ventas_etl(fechas)