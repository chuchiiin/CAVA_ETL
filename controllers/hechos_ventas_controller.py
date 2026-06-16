from fastapi import HTTPException, status
from typing import List
from models import HechosVentasModel, Venta, RangoFechas, ProductoVendido, HechosHistorialBotellaModel, PosicionDW
from controllers import DimBotellaController, DimFechaController


class HechosVentasController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosVentasModel(db_connection, dw_connection)
        self.historialbotella_model = HechosHistorialBotellaModel(db_connection, dw_connection)
        self.botella_controller = DimBotellaController(db_connection, dw_connection)
        self.fecha_controller = DimFechaController(dw_connection)

     
    def ventas_etl(self, fechas: RangoFechas):
        try:
            ventas_origen = self.model.get_ventas_para_hechos(fechas)

            cantidad_insertada = 0

            for venta_origen in ventas_origen:
                fecha = venta_origen.fecha_hora.date()
                hora = venta_origen.fecha_hora.time()

                self.fecha_controller.validar_fecha(fecha)

                venta_dw = Venta(
                    venta_id_original=venta_origen.id_venta,
                    botella_key=self.botella_controller.dbId_2_dwKey(
                        venta_origen.id_botella
                    ),
                    fecha_key=fecha,
                    hora=hora,
                    tipo=venta_origen.tipo,
                    ml=venta_origen.ml,
                    precio=venta_origen.registro_precio
                )

                insertadas = self.model.insertar_venta(venta_dw)
                cantidad_insertada += insertadas

            return {
                "mensaje": "ETL de ventas ejecutado correctamente",
                "cantidad_insertada": cantidad_insertada
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error durante el ETL de ventas: {str(e)}"
            )
        
    def nueva_venta(self, venta: List[ProductoVendido]):
        try:
            ventaDB = self.model.nueva_venta()
            for producto in venta:
                botella_key = self.botella_controller.dbId_2_dwKey(producto.id_botella)
                producto.id_venta = ventaDB["id_venta"]
                producto.registro_precio = self.botella_controller.get_botella_precio(producto.id_botella, producto.tipo)
                self.model.insertar_producto_vendido(producto)
                nuevo_estado = self.historialbotella_model.actualizar_ml_db(producto.ml, producto.id_botella)
                hecho_actual = self.historialbotella_model.get_historial_actual(botella_key)
                if(producto.tipo == "botella"):
                    hecho_nuevo = PosicionDW(
                        botella_key=botella_key,
                        tipo_evento="Venta botella",
                        estado="Vendida",
                        ml_restantes=nuevo_estado["ml_restantes"],
                        columna=hecho_actual["columna"],
                        fila=hecho_actual["fila"]
                    )
                else:
                    hecho_nuevo = PosicionDW(
                        botella_key=botella_key,
                        tipo_evento="Venta copa",
                        estado="Abierta",
                        ml_restantes=nuevo_estado["ml_restantes"],
                        columna=hecho_actual["columna"],
                        fila=hecho_actual["fila"]
                    )
                self.historialbotella_model.cambio_posicion_dw(hecho_nuevo)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error durante el ETL de ventas: {str(e)}"
            )