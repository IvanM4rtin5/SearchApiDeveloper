import sys
from fastapi import FastAPI
from loguru import logger

from app.api.search import router as search_router

# --- Configuração do Logging com Loguru ---
# Remove o handler padrão para evitar duplicação de logs.
logger.remove()
# Adiciona um novo handler para o stderr com um formato mais informativo.
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)
# --- Fim da Configuração do Logging ---

app = FastAPI(
    title="Search API for Developers",
    description="Uma API de busca federada para resolver problemas técnicos de desenvolvedores.",
    version="0.1.0",
)

app.include_router(search_router, prefix="/api/v1", tags=["Search"])