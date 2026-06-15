from fastapi import HTTPException, status
from models import HechosHistorialBotellaModel, AgregarBotella, Posicion, PosicionDW, DimBotellaModel

class HechosHistorialBotellaController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosHistorialBotellaModel(db_connection, dw_connection)
        self.botella_model = DimBotellaModel(db_connection, dw_connection)

    def agregar(self, botella: AgregarBotella):
        try:
            self.model.agregar(botella)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar el historial de la botella: {str(e)}"
            )
        
    def cambio_posicion(self, posicion: Posicion):
        try:
            posicion_cava = self.model.get_botella_posicion(posicion.columna, posicion.fila)
            actual_botella_key = self.botella_model.dbId_2_dwKey(posicion_cava["id_botella"])["botella_key"]
            if(posicion.id_botella == None):
                historial_actual = self.model.get_historial_actual(actual_botella_key)
                posicion_actual = PosicionDW(
                    botella_key=actual_botella_key,
                    tipo_evento="Retiro",
                    estado=historial_actual["estado"],
                    ml_restantes=historial_actual["ml_restantes"],
                )
                self.model.retiro_posicion_dw(posicion_actual)
            elif(posicion_cava["id_botella"] != posicion.id_botella):
                nueva_botella_key = self.botella_model.dbId_2_dwKey(posicion.id_botella)["botella_key"]
                self.model.cambio_posicion_db(posicion)
                historial_nuevo = self.model.get_historial_actual(nueva_botella_key)
                posicion_nueva = PosicionDW(
                    botella_key=nueva_botella_key,
                    tipo_evento="Cambio",
                    estado=historial_nuevo["estado"],
                    ml_restantes=historial_nuevo["ml_restantes"],
                    columna=posicion.columna,
                    fila=posicion.fila
                )
                historial_actual = self.model.get_historial_actual(actual_botella_key)
                posicion_actual = PosicionDW(
                    botella_key=actual_botella_key,
                    tipo_evento="Retiro",
                    estado=historial_actual["estado"],
                    ml_restantes=historial_actual["ml_restantes"],
                )
                self.model.cambio_posicion_dw(posicion_nueva)
                self.model.retiro_posicion_dw(posicion_actual)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar el historial de la botella: {str(e)}"
            )