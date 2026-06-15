from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date, datetime, time


class RangoFechas(BaseModel):
    fecha_inicio: Optional[date] = date.today()
    fecha_fin: Optional[date] = date.today()


class VentaOrigen(BaseModel):
    id_venta: str
    fecha_hora: datetime
    id_botella: int
    tipo: str
    ml: int
    registro_precio: float


class Venta(BaseModel):
    venta_id_original: str
    botella_key: int
    fecha_key: date
    hora: time
    tipo: str
    ml: int
    precio: float


class HechosVentasModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection
    

    def get_ventas_para_hechos(self, fechas: RangoFechas) -> List[VentaOrigen]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                SELECT 
                    v.id_venta,
                    v.fecha_hora,
                    pv.id_botella,
                    pv.tipo,
                    pv.ml,
                    pv.registro_precio
                FROM producto_vendido pv
                INNER JOIN venta v
                    ON pv.id_venta = v.id_venta
                WHERE v.fecha_hora::date BETWEEN '{fechas.fecha_inicio}' AND '{fechas.fecha_fin}'
                ORDER BY v.id_venta, pv.id_botella;
            """)

            rows = cur.fetchall()

        return [VentaOrigen(**row) for row in rows]
    

    def insertar_venta(self, venta: Venta) -> int:
       with self.dw.cursor() as cur:
            cur.execute(f"""
                INSERT INTO hechos_ventas(venta_id_original, botella_key, fecha_key, hora, tipo, ml, precio)
                SELECT '{venta.venta_id_original}','{venta.botella_key}','{venta.fecha_key}','{venta.hora}', '{venta.tipo}','{venta.ml}','{venta.precio}'
                WHERE NOT EXISTS (
                SELECT 1
                FROM hechos_ventas
                WHERE venta_id_original = '{venta.venta_id_original}'
                  AND botella_key = '{venta.botella_key}'
                );
                """)

            insertadas = cur.rowcount
            self.dw.commit()

       return insertadas
