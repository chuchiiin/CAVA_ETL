from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
        
class Botella(BaseModel):
    pedido_id: str
    lote: str
    vino_id: str
    cantidad: int = Field(gt=0, le=100)

class DimBotella(BaseModel):
    botella_id_original: int
    vino_key: int
    lote: str

class DimBotellaModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection

    def insertar_botella(self, botella: Botella, ml_restantes: int) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                INSERT INTO botella (pedido_id, lote, vino_id, ml_restantes, estado)
                VALUES ('{botella.pedido_id}','{botella.lote}','{botella.vino_id}',{ml_restantes},'llena')
                RETURNING *;
            """)
            return cur.fetchone()
    
    def insertar_dimBotella(self, botellaDB: DimBotella) -> List:
        with self.dw.cursor() as cur:
            cur.execute(f"""
                INSERT INTO dim_botella (botella_id_original, vino_key, lote)
                VALUES ('{botellaDB.botella_id_original}','{botellaDB.vino_key}','{botellaDB.lote}');
            """)
    