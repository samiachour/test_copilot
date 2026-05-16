from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import engine, Base
from .controllers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion des assets des employées")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
