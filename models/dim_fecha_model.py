from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class Fecha(BaseModel):
    fecha: Optional[date] = date.today()

class DimFechaModel:
    def __init__(self, dw_connection):
        self.dw = dw_connection

    def crear_fechas_mensuales(self, fecha: date):
        with self.dw.cursor() as cur:
            cur.execute(f"""
                WITH fechas as (
                    SELECT GENERATE_SERIES(
                        DATE_TRUNC('month', '{fecha}'::DATE),
                        DATE_TRUNC('month', '{fecha}'::DATE) + INTERVAL '1 month' - INTERVAL '1 day',
                        '1 day'::INTERVAL
                    )::DATE as fecha
                )
                INSERT INTO dim_fecha 
                SELECT fecha,
                    EXTRACT(YEAR FROM fecha) as anio,
                    EXTRACT(MONTH FROM fecha) as mes,
                    TO_CHAR(fecha, 'mon') as mes_nombre, 
                    EXTRACT(WEEK FROM fecha) as semana,
                    EXTRACT(DAY FROM fecha) as dia,
                    EXTRACT(ISODOW FROM fecha) as dia_semana,
                    TO_CHAR(fecha, 'day') as dia_nombre,
                    CASE WHEN EXTRACT(ISODOW FROM fecha) IN (6, 7) THEN true ELSE false END as fin_de_semana
                FROM fechas
                ON CONFLICT (fecha_key) DO NOTHING;
            """)