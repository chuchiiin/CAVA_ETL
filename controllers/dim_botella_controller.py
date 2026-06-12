from fastapi import HTTPException, status
from models import DimBotellaModel, dimBotella, Botella
from controllers import DimVinoController

class DimBotellaController:
    def __init__(self, db_connection, dw_connection):
        self.model = DimBotellaModel(db_connection, dw_connection)
        self.vino_controller = DimVinoController(db_connection, dw_connection)

    def insertar_botella(self, botellas: Botella):
        try:
    #       botellaDW = dimBotella(**self.model.insertar_botella(botellas)[0])
    #       self.model.insertar_dimBotella(botellaDW)
            self.model.insertar_botella(botellas)
            Dim = dimBotella(
                vino_key=self.vino_controller.dbId_2_dwKey(botellas.vino_id),
            )
            self.model.insertar_dimBotella(Dim)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar datos: {str(e)}"
            )