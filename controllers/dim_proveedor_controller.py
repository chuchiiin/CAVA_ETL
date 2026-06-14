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
    
    def dbId_2_dwKey(self, dbId: str) -> int:
        try:
            dwKey = self.model.dbId_2_dwKey(dbId)
            if dwKey:
                return dwKey["proveedor_key"]
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El proveedor no existe en el DW: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la key del proveedor (posiblemente el proveedor no existe): {str(e)}"
            )
