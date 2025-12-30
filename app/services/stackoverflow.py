import httpx
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from app.core.config import settings
from app.schemas.response import SearchResult

STACKEXCHANGE_API_URL = "https://api.stackexchange.com/2.3/search/advanced"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def search_stackoverflow(query: str, limit: int) -> List[SearchResult]:
    """
    Busca no Stack Overflow usando a API oficial.
    """
    async with httpx.AsyncClient() as client:
        params = {
            "order": "desc",
            "sort": "relevance",
            "q": query,
            "site": "stackoverflow",
            "pagesize": limit,
            "filter": "withbody", # Filtro para incluir o corpo da pergunta para o snippet
        }
        if settings.STACKEXCHANGE_KEY:
            params["key"] = settings.STACKEXCHANGE_KEY

        try:
            logger.info(f"Buscando no Stack Overflow com a query: '{query}'")
            response = await client.get(STACKEXCHANGE_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return _normalize_results(data.get("items", []))
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro na requisição ao Stack Overflow: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar no Stack Overflow: {e}")
            return []


def _normalize_results(items: List[Dict[str, Any]]) -> List[SearchResult]:
    """
    Normaliza os resultados da API do Stack Exchange para o nosso schema SearchResult.
    """
    normalized = []
    for item in items:
        normalized.append(SearchResult(
            source="stackoverflow",
            title=item["title"],
            url=item["link"],
            snippet=item.get("body_markdown", "")[:250] + "...", # Pega os primeiros 250 caracteres do corpo
            raw_score=item["score"],
            tags=item.get("tags", []),
            score=0 # O score final será calculado depois
        ))
    return normalized