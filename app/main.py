from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api import router
from .db import Base, engine
from .config import CONFIG
from .logging_cfg import configure_logging
import logging

# configure logging
configure_logging(CONFIG["logging"])
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    logger.info("Banco e tabelas inicializadas")
    yield
    # Shutdown
    logger.info("Aplicação encerrando")

app = FastAPI(title=CONFIG["app"]["title"], lifespan=lifespan)

# incluir rotas
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Sistema de Agendamento - API running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
