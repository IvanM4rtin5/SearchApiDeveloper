from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class SearchResult(BaseModel):
    source: str = Field(..., description="Fonte do resultado (ex: 'stackoverflow').")
    title: str = Field(..., description="Título do artigo, pergunta ou vídeo.")
    url: HttpUrl = Field(..., description="Link para o recurso original.")
    snippet: Optional[str] = Field(None, description="Pequeno trecho ou resumo do conteúdo.")
    score: float = Field(..., description="Pontuação de relevância calculada.")
    raw_score: Optional[float] = Field(None, description="Pontuação original da fonte (upvotes, likes, etc).")
    tags: Optional[List[str]] = Field(None, description="Tags ou categorias associadas.")


class SearchResponse(BaseModel):
    query: str = Field(..., description="Query original que gerou os resultados.")
    results: List[SearchResult] = Field(..., description="Lista de resultados da busca, ordenados por relevância.")