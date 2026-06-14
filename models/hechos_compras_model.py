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

class RangoFechas(BaseModel):
    fecha_inicio: Optional[date] = date.today()
    fecha_fin: Optional[date] = date.today()

class Compra(BaseModel):
    pedido_id_original: str
    provedor_key: int
    fecha_key: date
    precio_unitario: float
    botella_key: int
    fecha_entrega_key: Optional[date]

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

    def get_compras_rango(self, fechas: RangoFechas) -> List[Dict[str, Any]]:
        with self.db.cursor() as cur:
            cur.execute(f"""
                SELECT b.pedido_id, proveedor_id, fecha_pedido, costo_unitario, id_botella, fecha_entrega
                FROM botella as b
                INNER JOIN pedido as p ON p.pedido_id = b.pedido_id
                INNER JOIN producto_pedido as pp ON pp.pedido_id = b.pedido_id AND pp.lote = b.lote AND pp.vino_id = b.vino_id
                WHERE fecha_pedido BETWEEN '{fechas.fecha_inicio}' AND '{fechas.fecha_fin}';
            """)
            return cur.fetchall()

    def insertar_compra(self, compra: Compra):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                INSERT INTO hechos_compras(pedido_id_original, proveedor_key, fecha_key, precio_unitario, botella_key, fecha_entrega_key)
                VALUES ('{compra.pedido_id_original}',{compra.provedor_key},'{compra.fecha_key}',{compra.precio_unitario},{compra.botella_key},'{compra.fecha_entrega_key}');
            """)