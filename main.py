from core import settings, db_manager, dw_manager
from routes import *
from contextlib import asynccontextmanager
from fastapi import FastAPI

#ESTO ES EL CICLO DE VIDA DE LA APLICACIÓN PERO EN ASYNC PARA Q JALE MÁS CHIDO
#XD EL ASYNC ES PARA Q PUEDA MANEJAR MEJOR LAS CONEXIONES

#ciclo de vida para db
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Inicio")
    db_manager.connect()
    dw_manager.connect()
    yield #indicacion que el sistema usa para terminar el proceso (espera a que se llamen las rutas)
    db_manager.close_all()
    dw_manager.close_all()
    print("fin")


app = FastAPI(lifespan=lifespan)

app.include_router(live_router)
app.include_router(scheduled_router)

@app.get("/")
def root():
    return {"message": "Hola Mundo", "status": "ok"}