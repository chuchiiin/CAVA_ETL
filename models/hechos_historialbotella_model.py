from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class AgregarBotella(BaseModel):
    botella_key: int
    ml_restantes: int

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