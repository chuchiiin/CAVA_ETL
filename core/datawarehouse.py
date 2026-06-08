import psycopg2
from psycopg2 import pool, extensions, sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any, List
from .config import settings

class DataWarehouseManager:
    #INICIA EL MANEJAR DE CONEXIONES
    def __init__(self):
        self._pool: Optional[pool.SimpleConnectionPool] = None

    def connect(self):
        self._pool = pool.SimpleConnectionPool(
            minconn=settings.DW_POOL_MIN_SIZE,
            maxconn=settings.DW_POOL_MAX_SIZE,
            host=settings.DW_HOST,
            port=settings.DW_PORT,
            dbname=settings.DW_NAME,
            user=settings.DW_USER,
            password=settings.DW_PASSWORD,
            cursor_factory=RealDictCursor
        )

    #ESTO MANEJA LAS CONEXIONES Y LAS PRESTA
    @contextmanager
    def get_connection(self) -> Generator[extensions.connection, None, None]:
        conn = self._pool.getconn()
        try:
            #EL YIELD PRESTA LAS CONEXIONES DENTRO DEL WITH DONDE SE INVOQUEN
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    @contextmanager
    def get_cursor(self, conn=None):
        if conn is None:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    yield cursor
        else:
            with conn.cursor() as cursor:
                yield cursor

    def close_all(self):
        if self._pool:
            self._pool.closeall()

#LO MISMO DEL SINGLETON Y ESO
dw_manager = DataWarehouseManager()

#ACA PARA USARLO CUANDO SE VAYA A ABRIR LAS CONEXIONES
def get_dw():
    with dw_manager.get_connection() as conn:
        yield conn