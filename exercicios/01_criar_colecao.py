"""
Exercício 01 — Conectar ao Qdrant e criar a coleção.

Antes de carregar documentos, precisamos garantir que existe uma
coleção no Qdrant com a mesma dimensão do modelo de embeddings.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


# Carrega o .env da raiz do repositório, independente do diretório de execução.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Endereço do Qdrant publicado na porta 2222 da máquina OCI.
QDRANT_URL = os.getenv("QDRANT_URL", "http://146.235.55.187:2222")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
COLECAO = os.getenv("COLECAO", "documentos-ragestagio")

# Dimensão do modelo paraphrase-multilingual-MiniLM-L12-v2.
DIMENSAO = 384


def main() -> None:
    # O client fala com a API REST do Qdrant (porta 2222 -> 6333).
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Se a coleção já existir, recria do zero para começar limpo.
    if client.collection_exists(COLECAO):
        client.delete_collection(COLECAO)
        print(f"Coleção '{COLECAO}' removida.")

    client.create_collection(
        collection_name=COLECAO,
        vectors_config=VectorParams(
            size=DIMENSAO,
            distance=Distance.COSINE,
        ),
    )

    print(f"Coleção '{COLECAO}' criada em {QDRANT_URL}.")
    print(f"Dimensão: {DIMENSAO} | Métrica: COSINE")

    info = client.get_collection(COLECAO)
    print(f"Quantidade de pontos: {info.points_count}")


if __name__ == "__main__":
    main()
