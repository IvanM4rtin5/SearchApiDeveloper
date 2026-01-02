import asyncio
from fastapi import APIRouter, Query

from typing import List, Optional
from app.schemas.request import  SearchProvider
from app.schemas.response import SearchResponse
from app.services import stackoverflow, devto
from app.core.ranking import rank_results

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
async def search(
    query: str,
    sources: Optional[List[SearchProvider]] = Query(None),
    limit: int = 10
):
    provider_map = {
        SearchProvider.STACKOVERFLOW: stackoverflow.search_stackoverflow,
        SearchProvider.DEVTO: devto.search_devto,
    }

    if not sources:
        sources = list(provider_map.keys())

    tasks = [
        provider_map[source](query, limit)
        for source in sources
        if source in provider_map
    ]

    results = await asyncio.gather(*tasks)
    flat_results = [item for sublist in results for item in sublist]

    ranked_results = rank_results(flat_results)

    return SearchResponse(query=query, results=ranked_results)
