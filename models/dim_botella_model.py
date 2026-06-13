from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
        
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
        botellas_insertadas = []

        with self.db.cursor() as cur:
            
            contador = 0

            while contador < botella.cantidad:
                cur.execute(f"""
                     INSERT INTO botella (pedido_id, lote, vino_id, ml_restantes, estado)
                     VALUES ('{botella.pedido_id}','{botella.lote}','{botella.vino_id}','{botella.ml_restantes}','{botella.estado}')
                     
                     RETURNING id_botella, vino_id, lote;
                     """)

                botellas_insertadas.append(cur.fetchone())

                contador += 1

            self.db.commit()
        return botellas_insertadas
    
    def insertar_dimBotella(self, botellaDB: dimBotella) -> List:
        with self.dw.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO dim_botella (botella_id_original,vino_key, lote)
                    VALUES ('{botellaDB.botella_id_original}','{botellaDB.vino_key}','{botellaDB.lote}');
                    """)
                
        self.db.commit()
           
        return {
            "mensaje": "Dim botella insertada correctamente"
        }
    