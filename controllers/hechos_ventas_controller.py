from fastapi import HTTPException, status
from models import HechosVentasModel, Venta, RangoFechas
from controllers import DimBotellaController, DimFechaController


class HechosVentasController:
    def __init__(self, db_connection, dw_connection):
        self.model = HechosVentasModel(db_connection, dw_connection)
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

                self.model.insertar_venta(venta_dw)
                cantidad_insertada += 1

            return {
                "mensaje": "ETL de ventas ejecutado correctamente",
                "cantidad_insertada": cantidad_insertada
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error durante el ETL de ventas: {str(e)}"
            )