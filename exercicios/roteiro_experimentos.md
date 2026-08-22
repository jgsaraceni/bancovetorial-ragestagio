# Roteiro de experimentos — Qdrant

Preencha uma tabela para cada teste:

| Pergunta | Chunk | Overlap | Top-k | Evidência apareceu? | Redundância? | Fonte correta? | Latência |
|---|---:|---:|---:|---|---|---|---:|
| | | | | | | | |

## Experimento 1 — pergunta direta

```text
Quantas horas possui o estágio obrigatório?
```

Observe:

- o trecho com a carga horária aparece?
- em qual posição?
- a página está correta?

## Experimento 2 — paráfrase

```text
Qual é a duração exigida para o estágio curricular?
```

Compare com a pergunta anterior. Verifique se a busca recupera a mesma
evidência sem repetir as mesmas palavras do documento.

## Experimento 3 — pergunta sobre a disciplina

```text
A disciplina de Banco de Dados aborda otimização de consultas?
```

Observe se o resultado vem da ficha da disciplina ou de outro documento.

## Experimento 4 — ambiguidade

```text
Qual é a frequência mínima?
```

Discuta:

- a pergunta especifica o escopo?
- aparecem regras de documentos diferentes?
- a recuperação está errada ou a consulta é insuficiente?

## Experimento 5 — tamanho do chunk

Compare:

```python
TAMANHO_CHUNK = 400
SOBREPOSICAO = 50
```

com:

```python
TAMANHO_CHUNK = 1000
SOBREPOSICAO = 200
```

Depois de mudar o chunking, rode novamente:

```bash
python exercicios/01_criar_colecao.py
python exercicios/02_carregar_documentos.py
```

Observe:

- corte de frases;
- perda de contexto;
- mistura de assuntos;
- quantidade total de chunks.

## Experimento 6 — top-k

Compare:

```python
TOP_K = 1
TOP_K = 3
TOP_K = 8
```

Observe:

- cobertura;
- redundância;
- aparecimento de trechos irrelevantes;
- latência.

## Fechamento

Responder em grupo:

1. O primeiro resultado era semanticamente parecido ou realmente relevante?
2. A evidência necessária estava completa no chunk?
3. O aumento de top-k ajudou ou introduziu ruído?
4. O problema observado ocorreu na ingestão, no chunking, na indexação ou na busca?
