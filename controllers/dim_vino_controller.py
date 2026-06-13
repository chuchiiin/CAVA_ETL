from typing import List, Dict, Any
from fastapi import HTTPException, status
from models import DimVinoModel, Vino, DimVino

class DimVinoController:
    def __init__(self, db_connection, dw_connection):
        self.model = DimVinoModel(db_connection, dw_connection)

    def insertar_vino(self, vino: Vino) -> List[Dict[str, Any]]:
        try:
            vinoDB = DimVino (**self.model.insertar_vino(vino)[0])
            self.model.insertar_dimVino(vinoDB)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar los datos: {str(e)}"
            )
    
    def dbId_2_dwKey(self, dbId: str) -> int:
        try:
            dwKey = self.model.dbId_2_dwKey(dbId)
            if dwKey:
                return dwKey
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El vino no existe en el DW: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la key del vino (posiblemente el vino no existe): {str(e)}"
            )
        
    def get_total_ml(self, vino_id: str) -> int:
        try:
            ml = self.model.get_total_ml(vino_id)
            if ml:
                return ml
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"El vino no existe en el DW: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener los ml del vino: {str(e)}"
            )