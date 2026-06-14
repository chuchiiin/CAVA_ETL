from fastapi import HTTPException, status
from models import HechosComprasModel, Pedido, Botella, RangoFechas, Compra
from controllers import DimBotellaController, DimProveedorController

class HechosComprasController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosComprasModel(db_connection, dw_connection)
        self.botella_controller = DimBotellaController(db_connection, dw_connection)
        self.proveedor_controller = DimProveedorController(db_connection, dw_connection)

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
        
    def compras_etl(self, fechas: RangoFechas):
        try:
            registros = self.model.get_compras_rango(fechas)
            for registro in registros:
                compra = Compra(
                    pedido_id_original=registro["pedido_id"],
                    provedor_key=self.proveedor_controller.dbId_2_dwKey(registro["proveedor_id"]),
                    fecha_key=registro["fecha_pedido"],
                    precio_unitario=registro["costo_unitario"],
                    botella_key=self.botella_controller.dbId_2_dwKey(registro["id_botella"]),
                    fecha_entrega_key=registro["fecha_entrega"]
                )
                self.model.insertar_compra(compra)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error durante el etl de compras: {str(e)}"
            )
