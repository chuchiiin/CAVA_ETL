from fastapi import HTTPException, status
from models import DimBotellaModel, DimBotella, Botella, AgregarBotella
from controllers.dim_vino_controller import DimVinoController
from controllers.hechos_historialbotella_controller import HechosHistorialBotellaController

class DimBotellaController:
    def __init__(self, db_connection, dw_connection):
        self.model = DimBotellaModel(db_connection, dw_connection)
        self.vino_controller = DimVinoController(db_connection, dw_connection)
        self.historialbotella_controller = HechosHistorialBotellaController(db_connection, dw_connection)

    def insertar_botella(self, botellas: Botella):
        try:
            ml = self.vino_controller.get_total_ml(botellas.vino_id)
            for _ in range(botellas.cantidad):
                botella_insertada = self.model.insertar_botella(botellas, ml)
                dimBotella = DimBotella(
                    botella_id_original = botella_insertada["id_botella"],
                    lote = botellas.lote,
                    vino_key=self.vino_controller.dbId_2_dwKey(botellas.vino_id)
                )
                historial = AgregarBotella(
                    botella_key=self.model.insertar_dimBotella(dimBotella)["botella_key"],
                    ml_restantes=ml,
                )
                self.historialbotella_controller.agregar(historial)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar datos: {str(e)}"
            )
        
    def dbId_2_dwKey(self, dbId: int) -> int:
        try:
            dwKey = self.model.dbId_2_dwKey(dbId)
            if dwKey:
                return dwKey["botella_key"]
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La botella no existe en el DW: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener la key de la botella (posiblemente la botella no existe): {str(e)}"
            )