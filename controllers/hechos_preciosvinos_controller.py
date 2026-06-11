from fastapi import HTTPException, status
from models import HechosPreciosVinosModel, PrecioVino, HechoPrecioVino
from controllers import DimFechaController, DimVinoController
from datetime import date

class HechosPreciosVinosController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosPreciosVinosModel(db_connection, dw_connection)
        self.fecha_controller = DimFechaController(dw_connection)
        self.vino_controller = DimVinoController(db_connection, dw_connection)

    def actualizar_precio(self, precios: PrecioVino):
        try:
            self.fecha_controller.validar_fecha(date.today())
            self.model.actualizar_precio(precios)
            hecho = HechoPrecioVino(
                vino_key=self.vino_controller.dbId_2_dwKey(precios.vino_id),
                fecha_key=date.today(),
                precio_botella=precios.precio_botella,
                precio_copa=precios.precio_copa
            )
            self.model.insertar_hecho(hecho)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar los precios: {str(e)}"
            )