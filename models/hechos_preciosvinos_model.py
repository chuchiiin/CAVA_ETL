from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class PrecioVino(BaseModel):
    vino_id: str
    precio_botella: float
    precio_copa: float

class HechoPrecioVino(BaseModel):
    vino_key: int
    fecha_key: date
    precio_botella: float
    precio_copa: float

class HechosPreciosVinosModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection

    def actualizar_precio(self, precios: PrecioVino):
        with self.db.cursor() as cur:
            cur.execute(f"""
                UPDATE vino
                SET precio_botella = {precios.precio_botella}, precio_copa = {precios.precio_copa}
                WHERE vino_id = '{precios.vino_id}';
            """)

    def insertar_hecho(self, hecho: HechoPrecioVino):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                UPDATE hechos_preciosvinos SET actual = false WHERE actual = true AND vino_key = {hecho.vino_key};
                INSERT INTO hechos_preciosvinos(vino_key, fecha_key, actual, precio_botella, precio_copa)
                VALUES ({hecho.vino_key}, '{hecho.fecha_key}', true, {hecho.precio_botella}, {hecho.precio_copa});
            """)