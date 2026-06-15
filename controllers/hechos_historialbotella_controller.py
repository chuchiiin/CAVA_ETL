from fastapi import HTTPException, status
from models import HechosHistorialBotellaModel, AgregarBotella

class HechosHistorialBotellaController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosHistorialBotellaModel(db_connection, dw_connection)

    def agregar(self, botella: AgregarBotella):
        try:
            self.model.agregar(botella)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar el historial de la botella: {str(e)}"
            )