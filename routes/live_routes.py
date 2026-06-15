from fastapi import APIRouter, Depends
from core import get_db, get_dw
from controllers import DimProveedorController, DimVinoController, HechosPreciosVinosController, DimBotellaController, HechosComprasController, HechosHistorialBotellaController
from models import Proveedor, Vino, PrecioVino, Pedido, Posicion

router = APIRouter(prefix="/live", tags=["Live"])



def proveedor_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return DimProveedorController(db, dw)

def vino_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return DimVinoController(db, dw)

def preciosvinos_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return HechosPreciosVinosController(db, dw)

def botella_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return DimBotellaController(db, dw)

def compras_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return HechosComprasController(db, dw)

def historialbotella_controller(db = Depends(get_db), dw = Depends(get_dw)):
    return HechosHistorialBotellaController(db, dw)


@router.post("/insertar_proveedor")
def insertar_proveedor(proveedor: Proveedor, controller: DimProveedorController = Depends(proveedor_controller)):
    return controller.insertar_proveedor(proveedor)

@router.post("/insertar_vino")
def insertar_vino(vino: Vino, controller: DimVinoController = Depends(vino_controller)):
    return controller.insertar_vino(vino)

@router.patch("/actualizar_precios")
def actualizar_precios(precios: PrecioVino, controller: HechosPreciosVinosController = Depends(preciosvinos_controller)):
    return controller.actualizar_precio(precios)

@router.post("/insertar_pedido")
def insertar_pedido(pedido: Pedido, controller: HechosComprasController = Depends(compras_controller)):
    return controller.insertar_pedido_completo(pedido)

@router.patch("/cambiar_posicion")
def cambiar_posicion(posicion: Posicion, controller: HechosHistorialBotellaController = Depends(historialbotella_controller)):
    return controller.cambio_posicion(posicion)