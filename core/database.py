import psycopg2
from psycopg2 import pool, extensions, sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator, Optional, Dict, Any, List
from .config import settings

class DatabaseManager:
    #INICIA EL MANEJAR DE CONEXIONES
    def __init__(self):
        self._pool: Optional[pool.SimpleConnectionPool] = None

    def connect(self):
        self._pool = pool.SimpleConnectionPool(
            minconn=settings.DB_POOL_MIN_SIZE,
            maxconn=settings.DB_POOL_MAX_SIZE,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
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
db_manager = DatabaseManager()

#ACA PARA USARLO CUANDO SE VAYA A ABRIR LAS CONEXIONES
def get_db():
    with db_manager.get_connection() as conn:
        yield conn