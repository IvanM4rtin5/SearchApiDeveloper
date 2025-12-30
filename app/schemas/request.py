from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field


class SearchProvider(str, Enum):
    STACKOVERFLOW = "stackoverflow"
    DEVTO = "devto"
    YOUTUBE = "youtube"
    MEDIUM = "medium"


class SearchParams(BaseModel):
    query: str = Field(..., description="Problema técnico a ser pesquisado.")
    sources: Optional[List[SearchProvider]] = Field(None, description="Lista de fontes para a busca.")
    limit: int = Field(10, ge=1, le=50, description="Número máximo de resultados por fonte.")