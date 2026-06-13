from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class ProductoPedido(BaseModel):
    vino_id: str
    lote: str
    cantidad: int
    costo_unitario: float

class Pedido(BaseModel):
    proveedor_id: str
    fecha_pedido: Optional[date]
    fecha_entrega: Optional[date]
    productos: List[ProductoPedido]

class HechosComprasModel:
    def __init__(self, db_connection, dw_connection):
        self.db = db_connection
        self.dw = dw_connection

    def insertar_pedido(self, pedido: Pedido) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                INSERT INTO pedido(proveedor_id, fecha_pedido, fecha_entrega)
                VALUES ('{pedido.proveedor_id}', '{pedido.fecha_pedido}', '{pedido.fecha_entrega}')
                RETURNING *;
            """)
            return cur.fetchone()
        
    def insertar_producto_pedido(self, pedido_id: str, producto: ProductoPedido):
        with self.db.cursor() as cur:
            cur.execute(f"""
                INSERT INTO producto_pedido(pedido_id, lote, vino_id, cantidad, costo_unitario)
                VALUES('{pedido_id}', '{producto.lote}', '{producto.vino_id}', {producto.cantidad}, {producto.costo_unitario});
            """)
