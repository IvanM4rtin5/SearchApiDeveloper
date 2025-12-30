import asyncio
from app.core.ranking import rank_results
from app.schemas.response import SearchResult


async def search_stackoverflow(query: str, limit: int):
    return [
        SearchResult(
            source="stackoverflow",
            title="Erro de import no Python",
            url="https://stackoverflow.com/questions/12345",
            snippet="Erro ao importar módulos no Python.",
            raw_score=120,
            score=0,  # será recalculado no ranking
            tags=["python", "import", "error"],
        ),
        SearchResult(
            source="stackoverflow",
            title="ModuleNotFoundError ao importar módulo",
            url="https://stackoverflow.com/questions/67890",
            snippet="Como resolver erro de módulo não encontrado.",
            raw_score=95,
            score=0,
            tags=["python", "modules"],
        ),
    ]

async def search_devto(query: str, limit: int):
    return []

async def search_youtube(query: str, limit: int):
    return []

async def search_medium(query: str, limit: int):
    return []


async def main():
    results = await search_stackoverflow("erro import python", 10)
    ranked = rank_results(results)

    print("\nResultados ordenados:\n")
    for r in ranked:
        print(f"{r.source} | score={r.score:.2f}")
        print(r.title)
        print(r.url)
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())