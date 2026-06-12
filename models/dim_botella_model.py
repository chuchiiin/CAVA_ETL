from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
        
class producto_pedido(BaseModel):
   cantidad : int

class Botella(BaseModel):
    pedido_id: str
    lote: str
    vino_id: str
    ml_restantes: int
    estado: str
    cantidad: int = Field(gt=0, le=100)

class dimBotella(BaseModel):
    botella_id_original: int
    vino_key: int
    lote: str

class DimBotellaModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection

    def insertar_botella(self, botella: Botella) -> List:
        with self.db.cursor() as cur:
            
            contador = 0

            while contador < botella.cantidad:
             cur.execute(f"""
                INSERT INTO botella (pedido_id, lote, vino_id, ml_restantes, estado)
                values ('{botella.pedido_id}','{botella.lote}','{botella.vino_id}','{botella.ml_restantes}','{botella.estado}');
             """)

            contador += 1
        return cur.fetchall()
    
    def insertar_dimBotella(self, botellaDB: dimBotella, botella: Botella) -> List:
        with self.db.cursor() as cur:
            
            contador = 0

            while contador < botella.cantidad:
             cur.execute(f"""
                INSERT INTO dim_botella (botella_id_original, vino_key, lote)
                values ('{botellaDB.botella_id_original}','{botellaDB.vino_key}','{botellaDB.lote}');
             """)

            contador += 1
        return cur.fetchall()

    