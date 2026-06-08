from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Vino(BaseModel):
    nombre: str
    marca: str
    precio_botella: float
    precio_copa: float
    tipo: str
    region: str
    cosecha: str
    anejado: Optional [str]
    alcohol: float
    volumen: int
    descripcion: str

class DimVino(BaseModel):
    vino_id: str
    nombre: str
    marca: str
    tipo: str
    region: str
    cosecha: str
    anejado: Optional [str]
    alcohol: float
    volumen: int

class DimVinoModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection
        
    def insertar_vino(self, vino: Vino) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                INSERT INTO vino (nombre, marca, precio_botella, precio_copa, tipo, region, cosecha, anejado, alcohol, volumen, descripcion)
                VALUES ('{vino.nombre}', '{vino.marca}', '{vino.precio_botella}', '{vino.precio_copa}', '{vino.tipo}', 
                '{vino.region}','{vino.cosecha}', '{vino.anejado}', '{vino.alcohol}', '{vino.volumen}', '{vino.descripcion}')
                        
                RETURNING *;
            """)
            return cur.fetchall()
        
    def insertar_dimVino(self, vinoDB: DimVino):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                INSERT INTO dim_vino (vino_id_original, nombre, marca, tipo, region, cosecha, anejado, alcohol, volumen)
                VALUES ('{vinoDB.vino_id}', '{vinoDB.nombre}', '{vinoDB.marca}', '{vinoDB.tipo}', '{vinoDB.region}','{vinoDB.cosecha}', '{vinoDB.anejado}', '{vinoDB.alcohol}', '{vinoDB.volumen}');
            """)