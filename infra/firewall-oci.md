# Liberar a porta 2222 na OCI

Para acessar o Qdrant (porta 2222) de fora da sua máquina OCI, a porta precisa
estar liberada em **dois lugares**: no Security List da VCN e no firewall do
sistema operacional da VM.

---

## 1. Security List (rede da OCI)

1. Acesse o console da OCI → **Networking → Virtual cloud networks (VCNs)**.
2. Abra a sua VCN e depois o **Security List** associado à sub-rede pública.
3. Clique em **Add Ingress Rules**:
   - **Source CIDR:** `0.0.0.0/0` (acesso de qualquer lugar)
     ou um IP restrito (recomendado para produção).
   - **IP Protocol:** `TCP`.
   - **Destination Port Range:** `2222`.
4. Salve a regra.

> O Qdrant REST usa **TCP** na porta 2222. Não é UDP.

---

## 2. Firewall do sistema operacional (Oracle Linux)

Se a VM usa Oracle Linux com `firewalld`:

```bash
sudo firewall-cmd --permanent --add-port=2222/tcp
sudo firewall-cmd --reload
```

Se usa `iptables`:

```bash
sudo iptables -A INPUT -p tcp --dport 2222 -j ACCEPT
```

---

## 3. Confirmar o listener do container

Dentro da VM, confirme que o container está escutando na porta 2222:

```bash
docker ps
sudo ss -tlnp | grep 2222
```

Se aparecer `0.0.0.0:2222`, o mapeamento do container está ativo.

---

## 4. Teste final

De sua máquina local:

```bash
curl http://SEU_IP_OCI:2222/
```

Se receber a resposta JSON do Qdrant, a infraestrutura está pronta.
