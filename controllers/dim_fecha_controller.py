from fastapi import HTTPException, status
from models import DimFechaModel
from datetime import date

class DimFechaController:
    def __init__(self, dw_connection):
        self.model = DimFechaModel(dw_connection)

    def crear_fechas_mensuales(self, fecha: date):
        try:
            self.model.crear_fechas_mensuales(fecha)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar las fechas: {str(e)}"
            )
        
    def validar_fecha(self, fecha: date):
        try:
            if(self.model.fecha_existe(fecha) == None):
                self.model.crear_fechas_mensuales(fecha)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar las fechas: {str(e)}"
            )