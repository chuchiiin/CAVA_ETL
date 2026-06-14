from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Proveedor(BaseModel):
    nombre: str
    telefono: int
    correo: str
    especialidad: Optional[str]
    tiempo_promedio: Optional[str]
    anotacion: Optional[str]

class DimProveedor(BaseModel):
    proveedor_id: str
    nombre: str
    telefono: int
    correo: str
    especialidad: Optional[str]
    tiempo_promedio: Optional[str]
    anotacion: Optional[str]

class DimProveedorModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection
        
    def insertar_proveedor(self, proveedor: Proveedor) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                INSERT INTO proveedor (nombre, telefono, correo, especialidad, tiempo_promedio, anotacion) 
                VALUES ('{proveedor.nombre}',{proveedor.telefono},'{proveedor.correo}','{proveedor.especialidad}','{proveedor.tiempo_promedio}','{proveedor.anotacion}')
                        
                RETURNING *;
            """)
            return cur.fetchall()
        
    def insertar_dimProveedor(self, proveedorDB: DimProveedor):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                INSERT INTO dim_proveedor (proveedor_id_original, nombre, telefono, correo, especialidad, tiempo_promedio, anotacion) 
                VALUES ('{proveedorDB.proveedor_id}','{proveedorDB.nombre}','{proveedorDB.telefono}','{proveedorDB.correo}','{proveedorDB.especialidad}','{proveedorDB.tiempo_promedio}','{proveedorDB.anotacion}');
            """)

    def dbId_2_dwKey(self, dbId: str) -> List[Dict[str, Any]]:
        with self.dw.cursor() as cur:
            cur.execute(f"""
                SELECT proveedor_key FROM dim_proveedor WHERE proveedor_id_original = '{dbId}';
            """)
            return cur.fetchone()