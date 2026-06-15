from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class AgregarBotella(BaseModel):
    botella_key: int
    ml_restantes: int

class Posicion(BaseModel):
    id_botella: Optional[int] = None
    columna: str
    fila: str

class PosicionDW(BaseModel):
    botella_key: int
    tipo_evento: str
    estado: str
    ml_restantes: int
    columna: Optional[str] = None
    fila: Optional[str] = None

class HechosHistorialBotellaModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection

    def agregar(self, botella: AgregarBotella):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                INSERT INTO hechos_historialbotellas(botella_key, fecha_key, hora, actual, tipo_evento, estado, ml_restantes, columna, fila)
                VALUES ({botella.botella_key},NOW()::DATE,NOW(),true,'Agregada','Cerrada',{botella.ml_restantes},NULL,NULL);
            """)

    def cambio_posicion_dw(self, posicionDW: PosicionDW):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                UPDATE hechos_historialbotellas SET actual = false WHERE botella_key = {posicionDW.botella_key};
                INSERT INTO hechos_historialbotellas(botella_key, fecha_key, hora, actual, tipo_evento, estado, ml_restantes, columna, fila)
                VALUES ({posicionDW.botella_key},NOW()::DATE,NOW(),true,'{posicionDW.tipo_evento}','{posicionDW.estado}',{posicionDW.ml_restantes},'{posicionDW.columna}','{posicionDW.fila}');
            """)


    def retiro_posicion_dw(self, posicionDW: PosicionDW):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                UPDATE hechos_historialbotellas SET actual = false WHERE botella_key = {posicionDW.botella_key};
                INSERT INTO hechos_historialbotellas(botella_key, fecha_key, hora, actual, tipo_evento, estado, ml_restantes, columna, fila)
                VALUES ({posicionDW.botella_key},NOW()::DATE,NOW(),true,'{posicionDW.tipo_evento}','{posicionDW.estado}',{posicionDW.ml_restantes},NULL,NULL);
            """)

    def cambio_posicion_db(self, posicion: Posicion):
        with self.db.cursor() as cur:
            cur.execute(f"""
                UPDATE posicion_botella SET id_botella = {posicion.id_botella}
                WHERE columna = '{posicion.columna}' AND fila = '{posicion.fila}';
            """)

    def get_botella_posicion(self, columna: str, fila: str) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"SELECT * FROM posicion_botella WHERE columna = '{columna}' AND fila = '{fila}';")
            return cur.fetchone()
        
    def get_historial_actual(self, botella_key: int) -> List[Dict[str, Any]]:
        with self.dw.cursor() as cur:
            cur.execute(f"SELECT * FROM hechos_historialbotellas WHERE botella_key = {botella_key} AND actual = true;")
            return cur.fetchone()