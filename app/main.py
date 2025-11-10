from fastapi import FastAPI
from app.api import router
from app.db import Base, engine
from app.config import CONFIG
from app.logging_cfg import configure_logging
import logging

# configure logging
configure_logging(CONFIG["logging"])
logger = logging.getLogger(__name__)

app = FastAPI(title=CONFIG["app"]["title"])

# incluir rotas
app.include_router(router, prefix="/api")

@app.on_event("startup")
def startup():
    # cria tabelas
    Base.metadata.create_all(bind=engine)
    logger.info("Banco e tabelas inicializadas")

@app.get("/")
def root():
    return {"message": "Sistema de Agendamento - API running"}
