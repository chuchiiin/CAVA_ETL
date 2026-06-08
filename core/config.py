import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    load_dotenv()

    #BD
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int (os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "bd")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    #API (LA VDD NO CREO Q SE USE)
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    #LÍMITE DE CONEXIONES
    DB_POOL_MIN_SIZE: int = int(os.getenv("DB_POOL_MIN_SIZE", "1"))
    DB_POOL_MAX_SIZE: int = int(os.getenv("DB_POOL_MAX_SIZE", "3"))

    #DW
    DW_HOST: str = os.getenv("DW_HOST", "localhost")
    DW_PORT: int = int (os.getenv("DW_PORT", "5432"))
    DW_NAME: str = os.getenv("DW_NAME", "bd")
    DW_USER: str = os.getenv("DW_USER", "postgres")
    DW_PASSWORD: str = os.getenv("DW_PASSWORD", "")

    #LIMITE DE CONEXIONES
    DW_POOL_MIN_SIZE: int = int(os.getenv("DW_POOL_MINE_SIZE", "1"))
    DW_POOL_MAX_SIZE: int = int(os.getenv("DW_POOL_MAX_SIZE", "3"))

    #PROPPERTY CALCULA EL VALOR DE LA VARIABLE AL MOMENTO DE LLAMARLA
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DW_USER}:{self.DW_PASSWORD}@{self.DW_HOST}:{self.DW_PORT}/{self.DW_NAME}"

#SE LLAMA A SI MISMO PARA NO LLAMARSE EN TODOS LOS USOS (Según SINGLETON o algo así xd)
settings = Settings()