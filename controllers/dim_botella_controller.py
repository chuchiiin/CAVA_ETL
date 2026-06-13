from fastapi import HTTPException, status
from models import DimBotellaModel, DimBotella, Botella
from controllers import DimVinoController

class DimBotellaController:
    def __init__(self, db_connection, dw_connection):
        self.model = DimBotellaModel(db_connection, dw_connection)
        self.vino_controller = DimVinoController(db_connection, dw_connection)

    def insertar_botella(self, botellas: Botella):
        try:
            for _ in range(botellas.cantidad):
                botella_insertada = self.model.insertar_botella(botellas, self.vino_controller.get_total_ml(botellas.vino_id))
                dimBotella = DimBotella(
                    botella_id_original = botella_insertada["id_botella"],
                    lote = botellas.lote,
                    vino_key=self.vino_controller.dbId_2_dwKey(botellas.vino_id)
                )
                self.model.insertar_dimBotella(dimBotella)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar datos: {str(e)}"
            )