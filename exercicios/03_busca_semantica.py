"""
Exercício 03 — Busca semântica (queries) no Qdrant.

A pergunta é transformada no mesmo modelo de embeddings usado na
ingestão e comparada com os pontos da coleção usando cosseno.

Ajuste TOP_K e teste parafrases/ambiguidades conforme o roteiro.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


# Carrega o .env da raiz do repositório, independente do diretório de execução.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

QDRANT_URL = os.getenv("QDRANT_URL", "http://146.235.55.187:2222")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
COLECAO = os.getenv("COLECAO", "documentos-ragestagio")

# Quantidade de resultados retornados por query.
TOP_K = 5

MODELO = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def buscar(
    client: QdrantClient,
    modelo: SentenceTransformer,
    pergunta: str,
    top_k: int = TOP_K,
) -> None:
    embedding = modelo.encode(
        pergunta,
        normalize_embeddings=True,
    )

    resultado = client.query_points(
        collection_name=COLECAO,
        query=embedding.tolist(),
        limit=top_k,
        with_payload=True,
    )

    print(f"\nPergunta: {pergunta}\n")

    for posicao, ponto in enumerate(resultado.points, start=1):
        payload = ponto.payload
        score = ponto.score

        print(f"{posicao}. score={score:.4f}")
        print(
            f"   {payload['fonte']} "
            f"— página {payload['pagina']} "
            f"— chunk {payload['chunk']}"
        )
        print(f"   {payload['texto'][:500]}")
        print()


def main() -> None:
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    modelo = SentenceTransformer(MODELO)

    info = client.get_collection(COLECAO)
    print(f"Coleção '{COLECAO}' com {info.points_count} pontos.\n")

    while True:
        pergunta = input(
            "Digite sua pergunta ou 'sair': "
        ).strip()

        if pergunta.lower() == "sair":
            print("Programa encerrado.")
            break

        if not pergunta:
            print("Digite uma pergunta válida.")
            continue

        buscar(client, modelo, pergunta)


if __name__ == "__main__":
    main()
