"""
Exercício 02 — Carregar documentos no Qdrant.

Fluxo de ingestão:

PDF
  -> páginas
  -> chunks (com sobreposição)
  -> embeddings (modelo multilíngue)
  -> pontos no Qdrant

Ajuste TAMANHO_CHUNK e SOBREPOSICAO e observe como muda a
quantidade total de chunks (experimento 5 da disciplina).
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:2222")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") or None
COLECAO = os.getenv("COLECAO", "documentos-ragestagio")

# Pasta onde ficam os PDFs da disciplina.
PASTA_DOCUMENTOS = Path("data/documentos")

# Tamanho (caracteres) e sobreposição de cada chunk.
TAMANHO_CHUNK = 800
SOBREPOSICAO = 150

MODELO = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def carregar_paginas(caminho: Path) -> list[dict]:
    leitor = PdfReader(caminho)
    paginas = []

    for numero, pagina in enumerate(leitor.pages, start=1):
        texto = pagina.extract_text() or ""

        if texto.strip():
            paginas.append(
                {
                    "fonte": caminho.name,
                    "pagina": numero,
                    "texto": texto.strip(),
                }
            )

    return paginas


def gerar_chunks(
    texto: str,
    tamanho: int = TAMANHO_CHUNK,
    sobreposicao: int = SOBREPOSICAO,
) -> list[str]:
    if tamanho <= sobreposicao:
        raise ValueError("O tamanho deve ser maior que a sobreposição.")

    chunks = []
    inicio = 0

    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        trecho = texto[inicio:fim].strip()

        if trecho:
            chunks.append(trecho)

        if fim == len(texto):
            break

        inicio = fim - sobreposicao

    return chunks


def main() -> None:
    if not PASTA_DOCUMENTOS.exists():
        raise FileNotFoundError(
            f"Pasta não encontrada: {PASTA_DOCUMENTOS.resolve()}"
        )

    arquivos = sorted(PASTA_DOCUMENTOS.glob("*.pdf"))

    if not arquivos:
        raise FileNotFoundError(
            "Nenhum PDF encontrado em "
            f"{PASTA_DOCUMENTOS.resolve()}"
        )

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    modelo = SentenceTransformer(MODELO)

    pontos = []

    for arquivo in arquivos:
        print(f"\nProcessando: {arquivo.name}")

        for pagina in carregar_paginas(arquivo):
            chunks = gerar_chunks(pagina["texto"])

            for numero_chunk, chunk in enumerate(chunks):
                identificador = (
                    f"{arquivo.stem}"
                    f"-p{pagina['pagina']}"
                    f"-c{numero_chunk}"
                )
                pontos.append(
                    {
                        "id": identificador,
                        "texto": chunk,
                        "fonte": pagina["fonte"],
                        "pagina": pagina["pagina"],
                        "chunk": numero_chunk,
                    }
                )

    textos = [ponto["texto"] for ponto in pontos]

    print(f"\nGerando embeddings para {len(textos)} chunks...")
    embeddings = modelo.encode(
        textos,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    vetores = [
        {
            "id": ponto["id"],
            "vector": embedding.tolist(),
            "payload": {
                "texto": ponto["texto"],
                "fonte": ponto["fonte"],
                "pagina": ponto["pagina"],
                "chunk": ponto["chunk"],
            },
        }
        for ponto, embedding in zip(pontos, embeddings)
    ]

    # Upsert em lotes de 100 pontos.
    for inicio in range(0, len(vetores), 100):
        client.upsert(
            collection_name=COLECAO,
            points=vetores[inicio:inicio + 100],
        )

    print(f"\n{len(vetores)} pontos enviados para a coleção '{COLECAO}'.")

    info = client.get_collection(COLECAO)
    print(f"Total de pontos na coleção: {info.points_count}")


if __name__ == "__main__":
    main()
