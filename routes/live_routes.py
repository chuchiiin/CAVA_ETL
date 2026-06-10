from fastapi import APIRouter, Depends
from core import get_db, get_dw
from controllers import DimProveedorController, DimVinoController
from models import Proveedor, Vino

router = APIRouter(prefix="/live", tags=["Live"])



def proveedor_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return DimProveedorController(db, dw)

@router.post("/insertar_proveedor")
def insertar_proveedor(proveedor: Proveedor, controller: DimProveedorController = Depends(proveedor_controller)):
    return controller.insertar_proveedor(proveedor)



def vino_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return DimVinoController(db,dw)

@router.post("/insertar_vino")
def insertar_vino(vino: Vino, controller: DimVinoController = Depends(vino_controller)):
    return controller.insertar_vino(vino)
