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