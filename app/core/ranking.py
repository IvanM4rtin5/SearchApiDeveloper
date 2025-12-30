from typing import List
from app.schemas.response import SearchResult

# Pesos iniciais para as fontes. Pode ser ajustado conforme a percepção de qualidade.
SOURCE_WEIGHTS = {
    "stackoverflow": 1.0,
    "devto": 0.8,
    "youtube": 0.7,
    "medium": 0.9,
}


def rank_results(results: List[SearchResult]) -> List[SearchResult]:
    """
    Calcula o score final e ordena os resultados.

    MVP Ranking Logic:
    - Relevância: A API do provedor já retorna ordenado por relevância (peso 0.5).
    - Popularidade: `raw_score` (upvotes, likes) normalizado (peso 0.3).
    - Peso da Fonte: Um valor fixo por provedor (peso 0.2).
    """
    if not results:
        return []

    for result in results:
        popularity = result.raw_score or 0
        source_weight = SOURCE_WEIGHTS.get(result.source, 0.5)
        # A relevância do texto já é considerada na ordem que a API externa retorna.
        # Esta é uma fórmula simplificada para o MVP.
        result.score = (popularity * 0.3) + (source_weight * 100 * 0.2) # Multiplicador para dar mais peso à fonte

    # Ordena os resultados pelo score final, do maior para o menor.
    return sorted(results, key=lambda r: r.score, reverse=True)