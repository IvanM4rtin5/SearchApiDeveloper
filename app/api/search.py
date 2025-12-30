import asyncio
from fastapi import APIRouter, Depends

from app.schemas.request import SearchParams, SearchProvider
from app.schemas.response import SearchResponse
from app.services import stackoverflow
from app.core.ranking import rank_results

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
async def search(params: SearchParams = Depends()):
    """
    Executa uma busca federada por um problema técnico em diversas fontes.
    """
    # Mapeia os provedores de busca para suas respectivas funções de serviço.
    provider_map = {
        SearchProvider.STACKOVERFLOW: stackoverflow.search_stackoverflow,
        # Outros provedores serão adicionados aqui.
    }

    # Se nenhuma fonte for especificada, busca em todas as disponíveis.
    sources_to_search = params.sources or list(provider_map.keys())

    # Cria uma lista de tarefas assíncronas para buscar em paralelo.
    tasks = [
        provider_map[source](params.query, params.limit)
        for source in sources_to_search if source in provider_map
    ]

    # Executa todas as buscas concorrentemente.
    results_from_providers = await asyncio.gather(*tasks)
    flat_results = [item for sublist in results_from_providers for item in sublist]

    # Aplica o ranking e retorna a resposta.
    ranked_results = rank_results(flat_results)

    return SearchResponse(query=params.query, results=ranked_results)