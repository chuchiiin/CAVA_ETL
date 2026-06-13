from fastapi import HTTPException, status
from models import DimBotellaModel, dimBotella, Botella
from controllers import DimVinoController

class DimBotellaController:
    def __init__(self, db_connection, dw_connection):
        self.model = DimBotellaModel(db_connection, dw_connection)
        self.vino_controller = DimVinoController(db_connection, dw_connection)

    def insertar_botella(self, botellas: Botella):
        try:
            botellas_insertadas = self.model.insertar_botella(botellas)

            for botella_insertada in botellas_insertadas:
                Dim = dimBotella(
                    botella_id_original = botella_insertada["id_botella"],
                    lote = botella_insertada["lote"],
                    vino_key=self.vino_controller.dbId_2_dwKey(botella_insertada["vino_id"])
                )

                self.model.insertar_dimBotella(Dim)
       
            return {
            "mensaje": "Botellas insertadas correctamente",
            "cantidad_insertada": botellas.cantidad
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar datos: {str(e)}"
            )