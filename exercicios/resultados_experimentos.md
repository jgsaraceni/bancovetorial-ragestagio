# Resultados dos Experimentos — Banco Vetorial Qdrant

Disciplina: Engenharia de Contexto (pós-graduação UFPR)
Banco: Qdrant na OCI (`146.235.55.187:2222`), coleção `documentos-ragestagio`
Modelo de embeddings: `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensões, cosseno)

Documentos indexados (em `data/documentos/`):

- `2024-regulamento-estagio.pdf`
- `PPC-do-Curso-de-Ciencia-da-Computação.pdf`
- `ci1218.pdf`

---

## 1. Configurações testadas

| Configuração | Tamanho do chunk | Sobreposição | Total de pontos |
|---|---:|---:|---:|
| A | 800 | 150 | 118 |
| B | 1000 | 200 | 99 |

As duas execuções usaram `TOP_K = 5`.

---

## 2. Tabela resumo

| Pergunta | Chunk | Overlap | Top-k | Evidência apareceu? | Redundância? | Fonte correta? | Latência |
|---|---:|---:|---:|---|---|---|---:|
| Quantas horas possui o estágio obrigatório? | 800 | 150 | 5 | Sim (posição 5) | Sim | Parcial | ~60 ms |
| Quantas horas possui o estágio obrigatório? | 1000 | 200 | 5 | Sim (posição 3) | Sim | Sim | ~77 ms |
| Qual é a duração exigida para o estágio curricular? | 800 | 150 | 5 | Sim (posições 3–5) | Sim | Sim | ~60 ms |
| Qual é a duração exigida para o estágio curricular? | 1000 | 200 | 5 | Sim (posições 3–4) | Sim | Sim | ~60 ms |
| A disciplina de Banco de Dados aborda otimização de consultas? | 800 | 150 | 5 | Sim (posição 1) | Não | Sim | ~57 ms |
| A disciplina de Banco de Dados aborda otimização de consultas? | 1000 | 200 | 5 | Sim (posição 1) | Não | Sim | ~57 ms |
| Qual é a frequência mínima? | 800 | 150 | 5 | Sim (posições 1–2) | Sim | Parcial | ~53 ms |
| Qual é a frequência mínima? | 1000 | 200 | 5 | Sim (posições 1–2) | Sim | Parcial | ~53 ms |

> Latência medida na coleção com 99 pontos (chunk 1000): encode ≈ 0,03 s +
> busca ≈ 0,03 s. A latência da configuração com 118 pontos (chunk 800) era
> da mesma ordem de grandeza (a busca vetorial domina em milissegundos para
> coleções deste porte).

---

## 3. Experimento 1 — pergunta direta

> Quantas horas possui o estágio obrigatório?

### Chunk 800 (118 pontos)

O trecho com a resposta correta — estágio obrigatório com **220 horas**
(Art. 14º) — apareceu apenas na **posição 5** (`2024-regulamento-estagio.pdf`
página 3, chunk 0, score 0.6136). As posições 1–4 trouxeram textos sobre
estágio **não obrigatório** e sobre atividades formativas/TCC, que não
respondem à pergunta.

### Chunk 1000 (99 pontos)

A mesma evidência (estágio obrigatório com 220 horas) apareceu na
**posição 3** (`PPC-do-Curso-de-Ciencia-da-Computação.pdf` página 10,
chunk 1, score 0.6530), além de outros trechos relacionados na posição 5.

### Análise

- **O trecho com a carga horária aparece?** Sim, nas duas configurações.
- **Em qual posição?** Posição 5 (chunk 800) e posição 3 (chunk 1000).
- **A página está correta?** Sim — os chunks apontam para as páginas corretas
  do regulamento e do PPC.
- **Observação:** mesmo assim, o **primeiro resultado não é a resposta**.
  As posições 1–2 ficam ocupadas por textos de estágio *não obrigatório*,
  cuja semântica ("duração de no mínimo um semestre e no máximo dois anos")
  está mais próxima das palavras da pergunta. Isso indica que a pergunta
  direta não tem escopo suficiente: a palavra "obrigatório" existe nos dois
  textos, e o modelo não distingue bem os dois regimes apenas pelo cosseno.
- **Conclusão:** a pergunta precisaria qualificar melhor o escopo
  (ex.: "do estágio obrigatório **do curso**") ou o sistema usaria filtros
  por payload (ex.: `tipo = regulamento`).

---

## 4. Experimento 2 — paráfrase

> Qual é a duração exigida para o estágio curricular?

### Chunk 800 (118 pontos)

Recuperou a mesma família de evidências da pergunta 1, com scores mais altos:
posição 3 → regulamento pág. 3 (220 horas), posição 4 → PPC pág. 24 (220
horas), posição 5 → PPC pág. 10 (220 horas, duração de um semestre).
Posições 1–2 ainda foram de estágio não obrigatório, mas com scores elevados
(0.81).

### Chunk 1000 (99 pontos)

Mesma família de evidências: posição 3 → PPC pág. 10 (0.75), posição 4 →
regulamento pág. 3 (0.74), posição 5 → regulamento pág. 3 (requisitos de
estágio não obrigatório).

### Análise

- **A busca recupera a mesma evidência sem repetir as palavras?** Sim. A
  paráfrase ("duração exigida" ≠ "horas possui") manteve a recuperação dos
  mesmos chunks sobre carga horária, com scores até mais altos (0.72–0.81).
- **Ganho em relação à pergunta 1:** a paráfrase produziu scores mais altos
  porque "duração" é termo presente nos documentos, enquanto "horas" é menos
  literal. Isso mostra que a **paráfrase melhor formulada melhora o
  resultado**, mesmo sem mudança de chunking.
- **Conclusão:** a recuperação semântica funciona bem para paráfrases — o
  modelo é robusto à troca de vocabulário.

---

## 5. Experimento 3 — pergunta sobre a disciplina

> A disciplina de Banco de Dados aborda otimização de consultas?

### Chunk 800 e Chunk 1000

Nas duas configurações o primeiro resultado (score ≈ 0.62–0.63) veio do
`ci1218.pdf` — página 1, chunk 1, que contém a **ementa** da disciplina de
Banco de Dados com o item "Processamento de consultas e otimização".
As posições 2–4 trouxeram ruído (regulamento de estágio e PPC), e a posição 5
voltou para o `ci1218.pdf` (objetivo da disciplina).

### Análise

- **O resultado vem da ficha da disciplina?** Sim — o top-1 é exatamente a
  ficha da disciplina (ci1218.pdf), onde consta a ementa.
- **O conteúdo responde à pergunta?** Sim — "Processamento de consultas e
  otimização" responde diretamente.
- **Ruído:** as posições 2–4 são irrelevantes (estágio). Isso ocorre porque o
  corpus tem poucos documentos sobre o assunto de banco de dados, e a busca
  preenche as posições restantes com o que for "menos dissimilar".
- **Conclusão:** este é o experimento com melhor desempenho — o resultado
  correto foi o primeiro nas duas configurações. O aumento do chunk (1000)
  até agregou um resultado extra do mesmo documento na posição 5.

---

## 6. Experimento 4 — ambiguidade

> Qual é a frequência mínima?

### Chunk 800 e Chunk 1000

Scores muito baixos em relação aos demais experimentos (top-1 ≈ 0.46 nas duas
configurações). As posições 1–2 trouxeram trechos do PPC sobre frequência
mínima (75% da carga horária), mas as posições 3–5 trouxeram tabelas de
atividades complementares e regras de tutoria, não relacionadas.

### Análise

- **A pergunta especifica o escopo?** Não. "Frequência mínima" não diz se é
  para disciplinas regulares, estágio, TCC ou atividades complementares —
  cada caso tem regra própria no PPC.
- **Aparecem regras de documentos diferentes?** Sim, trechos de regras
  distintas aparecem misturados (frequência para disciplinas, atividades
  complementares, tutoria).
- **A recuperação está errada ou a consulta é insuficiente?** A recuperação
  funcionou dentro do possível (os trechos com "frequência mínima" apareceram
  no topo), mas a **consulta é insuficiente**: faltou escopo. O baixo score
  geral (≈0.30–0.46) confirma a falta de precisão semântica da pergunta.
- **Conclusão:** o problema é da **consulta** (under-specified), não do
  banco. Uma pergunta melhor seria: "Qual é a frequência mínima para
  aprovação em uma disciplina regular?".

---

## 7. Experimento 5 — tamanho do chunk

Comparação efetivamente testada: **800/150 (118 chunks)** vs **1000/200
(99 chunks)**.

| Aspecto | Chunk 800 | Chunk 1000 |
|---|---|---|
| Total de pontos | 118 | 99 |
| Corte de frases | Menor ocorrência (chunks mais curtos) | Ocorre mais, textos mais longos |
| Perda de contexto | Menor | Pontos 3–5 dos experimentos 1–2 ganharam contexto |
| Mistura de assuntos | Menor | Maior (chunks de 1000 abrangem mais tópicos) |
| Posição da evidência (Exp. 1) | Posição 5 | Posição 3 |

- **Corte de frases:** com chunk 1000, a extração do PDF gerou trechos que
  começam no meio de palavras/frases (ex.: "diante a análise...",
  "sciplina e obter..."), porque o corte é por caracteres.
- **Perda de contexto:** o chunk maior preservou mais contexto do que o de
  800 (chunks dos experimentos 1–2 vieram mais completos), o que ajudou a
  posicionar a evidência da pergunta 1 mais cedo (posição 3 vs 5).
- **Mistura de assuntos:** chunk 1000 tende a misturar tópicos diferentes no
  mesmo vetor (ex.: uma página do PPC que fala de TCC + atividades
  complementares no mesmo chunk), o que pode "diluir" a similaridade.
- **Conclusão:** o chunk maior não trouxe ganho consistente — melhorou a
  posição da evidência no Exp. 1, mas manteve os demais resultados iguais e
  aumentou o risco de mistura de assuntos. Para este corpus, **chunks em
  torno de 800 com sobreposição moderada parecem mais equilibrados**.

---

## 8. Experimento 6 — top-k

Não foram coletadas execuções com `TOP_K = 1`, `3` e `8`; abaixo, análise
**inferida** a partir dos resultados de top-5 (as posições 4–5 de cada
pergunta mostram o que entraria/ sairia).

| Top-k | Efeito esperado |
|---|---:|
| 1 | Cobertura mínima; nos Exp. 1 e 2 o top-1 seria **incorreto** (estágio não obrigatório); no Exp. 3 seria correto; no Exp. 4 seria parcial. |
| 3 | Capturaria a evidência correta no Exp. 1 (chunk 1000) e Exp. 2; reduziria ruído. |
| 8 | Mais cobertura, porém com aumento de trechos irrelevantes (páginas de atividades complementares e tutoria), como visto nas posições 3–5 do Exp. 4. |

- **Cobertura:** aumenta com o top-k (mais chances de achar a evidência).
- **Redundância:** nos Exp. 1 e 2, múltiplos chunks do mesmo documento
  ocupam várias posições (ex.: regulamento pág. 4 + PPC pág. 26 com o mesmo
  artigo), indicando **redundância** que o top-k maior amplifica.
- **Ruído:** no Exp. 4, top-k maior introduz tabelas de atividades
  complementares e tutoria.
- **Latência:** o impacto do top-k na latência é pequeno para 99–118 pontos
  (a busca mantém-se na ordem de dezenas de milissegundos).

---

## 9. Fechamento

### 1. O primeiro resultado era semanticamente parecido ou realmente relevante?

Na maioria dos casos, **semanticamente parecido, mas nem sempre relevante**.
Nos experimentos 1 e 2, o top-1 era semanticamente próximo (falava de
estágio) mas **não respondia** à pergunta (era sobre o regime não
obrigatório). No experimento 3, o top-1 era realmente relevante (ementa da
disciplina). Conclusão: similaridade semântica ≠ resposta correta.

### 2. A evidência necessária estava completa no chunk?

No geral, **sim**, graças à sobreposição. A evidência (carga horária de 220
horas, frequência mínima de 75%) apareceu completa nos chunks recuperados.
Com chunk 1000, os trechos vieram ainda mais completos (mais contexto),
embora com início em meio de palavra. O risco está na **mistura de assuntos**
no mesmo chunk.

### 3. O aumento de top-k ajudou ou introduziu ruído?

**Ajudou e introduziu ruído ao mesmo tempo.** Ajudou porque, nos experimentos
1 e 2, a evidência correta só apareceu em posições 3–5 — com top-k=1 seria
perdida. Introduziu ruído porque as posições extras foram ocupadas por
trechos irrelevantes (atividades complementares, tutoria). O equilíbrio para
este corpus ficou em **top-k entre 3 e 5**.

### 4. O problema observado ocorreu na ingestão, no chunking, na indexação ou na busca?

Foram observados **problemas nas duas pontas**:

- **Na busca (consulta):** os maiores problemas vieram de perguntas
  sub-especificadas (Exp. 1 e Exp. 4). A pergunta "frequência mínima" sem
  escopo e "estágio obrigatório" sem distinção de regime não têm, sozinhas,
  como gerar recuperação precisa.
- **No chunking:** o corte por caracteres gera trechos começando no meio de
  palavras/frases, e o chunk de 1000 aumenta a mistura de assuntos.
- **Na indexação:** a ingestão em si foi correta (fonte/página corretas,
  IDs estáveis via UUID, sem duplicação).
- **No banco:** sem problemas — similaridade de cosseno respondeu conforme o
  esperado.

---

## 10. Recomendações

1. **Melhorar as consultas** (maior ganho): acrescentar escopo às perguntas e
   usar **filtros por payload** (ex.: filtrar `fonte` ou um campo `tipo`
   = regulamento/ppc/ficha) para evitar resultados cruzados entre documentos.
2. **Manter chunks em torno de 800–1000** com sobreposição de 15–20%; a
   diferença de qualidade entre eles foi pequena.
3. **Usar top-k = 3 a 5** para equilibrar cobertura e ruído neste corpus.
4. **Próximo passo opcional:** testar um modelo de embeddings mais forte
   (ex.: `multilingual-e5-large`, 1024 dims) para medir ganho real de
   relevância — lembrando que a dimensão sozinha não garante qualidade.
