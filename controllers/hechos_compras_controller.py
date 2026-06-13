from fastapi import HTTPException, status
from models import HechosComprasModel, Pedido, Botella
from controllers import DimBotellaController

class HechosComprasController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosComprasModel(db_connection, dw_connection)
        self.botella_controller = DimBotellaController(db_connection, dw_connection)

    def insertar_pedido_completo(self, pedido: Pedido):
        try:
            pedido_id = self.model.insertar_pedido(pedido)["pedido_id"]
            for producto in pedido.productos:
                self.model.insertar_producto_pedido(pedido_id, producto)
                botellas = Botella(
                    pedido_id=pedido_id,
                    lote=producto.lote,
                    vino_id=producto.vino_id,
                    cantidad=producto.cantidad
                )
                self.botella_controller.insertar_botella(botellas)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar pedido: {str(e)}"
            )
