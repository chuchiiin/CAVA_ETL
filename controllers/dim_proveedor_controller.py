from typing import List, Dict, Any
from fastapi import HTTPException, status
from models import DimProveedorModel, Proveedor, DimProveedor

class DimProveedorController:
    def __init__(self, db_connection, dw_connection):
        self.model = DimProveedorModel(db_connection, dw_connection)
        

    def insertar_proveedor(self, proveedor: Proveedor) -> List[Dict[str, Any]]:
        try:
            proveedorDB = DimProveedor(**self.model.insertar_proveedor(proveedor)[0])
            self.model.insertar_dimProveedor(proveedorDB)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar los datos: {str(e)}"
            )
    
