# Subir o Qdrant no Portainer (máquina OCI)

Este guia cria um container com o **Qdrant** no seu Portainer, exposto na
**porta 2222** do host (OCI).

O Qdrant por padrão escuta na porta **6333** (REST). O mapeamento
`2222:6333` publica o serviço na porta 2222 da máquina OCI.

---

## 1. Requisitos

- Portainer instalado e acessível na máquina OCI.
- A porta **2222** liberada no Security List / firewall da OCI
  (veja [`firewall-oci.md`](firewall-oci.md)).
- Este repositório clonado **ou** acesso ao GitHub
  (https://github.com/jgsaraceni/bancovetorial-ragestagio).

---

## 2. Opção A — Stack (docker-compose, recomendado)

A forma mais simples é criar um **Stack** no Portainer a partir do
[`docker-compose.yml`](docker-compose.yml) deste repositório.

### Pelo GitHub (Portainer conectado ao repositório)

1. No Portainer, acesse **Stacks → Add stack**.
2. Em **Name**, informe: `qdrant-ragestagio`.
3. Em **Build method**, escolha **Repository**.
4. Informe o repositório: `https://github.com/jgsaraceni/bancovetorial-ragestagio`
   (e a branch, se necessário, ex.: `main`).
5. Em **Repository path**, informe `infra`.
   O Portainer vai ler o arquivo `infra/docker-compose.yml`.
6. Clique em **Deploy the stack**.

### Colando o conteúdo manualmente

1. No Portainer, acesse **Stacks → Add stack**.
2. Em **Name**, informe: `qdrant-ragestagio`.
3. Em **Build method**, escolha **Web editor**.
4. Cole o conteúdo do arquivo `infra/docker-compose.yml`:

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant-ragestagio
    restart: unless-stopped
    ports:
      - "2222:6333"
    volumes:
      - qdrant_storage:/qdrant/storage
    environment:
      - QDRANT__SERVICE__GRPC_PORT=6334

volumes:
  qdrant_storage:
```

5. Clique em **Deploy the stack**.

---

## 3. Opção B — Container manual

Caso prefira criar o container direto:

1. No Portainer, acesse **Containers → Add container**.
2. Em **Name**: `qdrant-ragestagio`.
3. Em **Image**: `qdrant/qdrant:latest`.
4. Em **Port mapping**:
   - Host: `2222` → Container: `6333`
   - Tipo de protocolo: `TCP`
5. Em **Volumes**:
   - Volume: `qdrant_storage` → Bind: `/qdrant/storage`
6. Em **Restart policy**: `Unless stopped`.
7. Clique em **Deploy the container**.

---

## 4. Verificação

Depois do container rodando, teste o acesso:

- Dashboard web do Qdrant:
  `http://IP_DA_MAQUINA_OCI:2222/dashboard`
- Versão da API:
  `http://IP_DA_MAQUINA_OCI:2222/`

Exemplo:

```bash
curl http://SEU_IP_OCI:2222/
```

Deve responder algo como:

```json
{"title":"qdrant - vector search engine","version":"..."}
```

> **Dica:** se não responder, confira o `firewall-oci.md` — a porta 2222
> precisa estar liberada no Security List da OCI **e** no firewall do sistema
> operacional da VM.

---

## 5. Dados importantes

- **URL REST:** `http://SEU_IP_OCI:2222`
- **Porta interna (dentro do container):** `6333`
- **gRPC (opcional):** `6334`
- **Persistência:** volume Docker `qdrant_storage`
- **Conexão nos exercícios:** `QDRANT_URL` no arquivo `.env`
