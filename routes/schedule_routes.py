from fastapi import APIRouter, Depends
from core import get_db, get_dw
from controllers import DimVinoController

router = APIRouter(prefix="/Vino", tags=["Vino"])

def get_controllerDW(dw = Depends(get_dw)):
    return DimVinoController(dw)

@router.get("/")
def get_vino(controller: DimVinoController = Depends(get_controllerDW)):
    return controller.insertar_vino_controllers()

@router.get("/")
def get_dimVino(controller: DimVinoController = Depends(get_controllerDW)):
    return controller.insertar_dimVino_controller()
