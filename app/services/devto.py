import httpx
from typing import List, Dict, Any
from loguru import logger

from app.schemas.response import SearchResult

DEVTO_API_URL = "https://dev.to/api/articles"

async def search_devto(query: str, limit: int) -> List[SearchResult]:
    async with httpx.AsyncClient() as client:
        params = {
            "tag": query,
            "per_page": limit
        }

        try:
            response = await client.get(DEVTO_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return _normalize_results(data)
        
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro na requisição ao dev.to: {e.response.status_code} - {e.response.text}")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar no dev.to: {e}")
            return []


def _normalize_results(items: List[Dict[str, Any]]) -> List[SearchResult]:
    results = []

    for item in items:
        results.append(SearchResult(
            source="devto",
            title=item["title"],
            url=item["url"],
            snippet=item.get("description", "")[:250] + "...",
            raw_score=item.get("positive_reactions_count", 0),
            tags=item.get("tag_list", []),
            score=0
        ))

    return results
