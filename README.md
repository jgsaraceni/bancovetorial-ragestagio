# Banco Vetorial com Qdrant (RAG - Estágio)

Repositório da disciplina de **Engenharia de Contexto** (pós-graduação UFPR).

Este projeto sobe um **banco vetorial Qdrant** em um container Docker gerenciado
pelo **Portainer**, na máquina hospedada na **OCI (Oracle Cloud Infrastructure)**,
disponibilizado na **porta 2222**.

Depois da infraestrutura pronta, os exercícios carregam documentos (PDFs),
transformam em chunks + embeddings e realizam buscas semânticas (queries) no banco.

## Estrutura

```
bancovetorial-ragestagio/
├── README.md
├── .gitignore
├── requirements.txt
├── requirements-cpu.txt            # instala torch CPU-only (sem CUDA, mais leve)
├── docker-compose.yml              # Composição do Qdrant (porta 2222) — usada pelo Portainer
├── infra/
│   ├── portainer-qdrant.md         # Passo a passo: criar o container no Portainer (OCI)
│   └── firewall-oci.md             # Liberar a porta 2222 na OCI
├── data/
│   └── documentos/                 # PDFs usados nos exercícios
└── exercicios/
    ├── 01_criar_colecao.py         # Conecta no Qdrant e cria a coleção
    ├── 02_carregar_documentos.py   # Ingestão: PDF -> chunks -> embeddings -> Qdrant
    ├── 03_busca_semantica.py       # Queries (busca vetorial com top-k)
    └── roteiro_experimentos.md     # Roteiro de experimentos para preencher
```

## Começando

1. Siga o passo a passo de infraestrutura em [`infra/portainer-qdrant.md`](infra/portainer-qdrant.md).
2. Configure a porta 2222 na OCI conforme [`infra/firewall-oci.md`](infra/firewall-oci.md).
3. Instale as dependências. Prefira a versão CPU (mais leve, sem CUDA):
   ```bash
   pip install -r requirements-cpu.txt
   ```
   Use `pip install -r requirements.txt` apenas se quiser o torch com CUDA.
4. Crie o arquivo `.env` (fora do git) com `QDRANT_URL` e a mesma `QDRANT_API_KEY` definida na stack do Portainer.
5. Coloque os PDFs em `data/documentos/`.
6. Execute os exercícios em ordem:
   - `python exercicios/01_criar_colecao.py`
   - `python exercicios/02_carregar_documentos.py`
   - `python exercicios/03_busca_semantica.py`

> Obs.: os scripts usam o mesmo modelo de embeddings da disciplina
> (`paraphrase-multilingual-MiniLM-L12-v2`, 384 dimensões). Na primeira
> execução o modelo é baixado do Hugging Face.
