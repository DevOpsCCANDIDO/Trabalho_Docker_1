# Trabalho Docker Compose — Jogo de Adivinhação

Este repositório implementa uma aplicação simples de adivinhação com os componentes:

- Backend: Flask (Python) — cria jogos e processa palpites.
- Banco de Dados: Postgres (volume persistente).
- Frontend: React (Vite) servido via NGINX.
- NGINX: proxy reverso com balanceamento entre `backend1` e `backend2`.

URL de acesso local após subir com `docker-compose up`: http://localhost:8080

Comandos rápidos:

```bash
docker compose build
docker compose up -d
```

Para criar um jogo (exemplo):

```bash
curl -X POST -H "Content-Type: application/json" -d '{"secret":"abcde"}' http://localhost:8080/api/games
```

**Documentação rápida**

- **Arquitetura:** NGINX atua como servidor estático (frontend) e proxy reverso; dois backends Flask (`backend1`, `backend2`) servem a API em :5000; Postgres fornece persistência em volume `pgdata`.
- **Portas:** Host `:8080` → NGINX `:80`; backends expõem internamente `:5000` apenas.

**Como reconstruir e subir (local)**

1. Build das imagens:

```bash
docker compose build --no-cache
```

2. Subir stack em background:

```bash
docker compose up -d
```

3. Ver logs (ex.: nginx):

```bash
docker compose logs -f nginx
```

**Smoke tests (validados localmente)**

- Health check (via proxy):

```bash
curl http://localhost:8080/api/health
# -> {"status":"ok"}
```

- Criar jogo + enviar palpite (exemplo usado durante desenvolvimento):

```bash
python - <<'PY'
import json,urllib.request
data=json.dumps({'secret':'apple'}).encode()
req=urllib.request.Request('http://localhost:8080/api/games', data=data, headers={'Content-Type':'application/json'})
res=urllib.request.urlopen(req).read().decode()
print('CREATE_RESPONSE:', res)
game=json.loads(res)
id=game['game_id']
req2=urllib.request.Request(f'http://localhost:8080/api/games/{id}/guess', data=json.dumps({'guess':'apple'}).encode(), headers={'Content-Type':'application/json'})
res2=urllib.request.urlopen(req2).read().decode()
print('GUESS_RESPONSE:', res2)
PY
```

**Troubleshooting comum**

- 502 Bad Gateway no NGINX: verifique logs do `nginx` e dos backends (`docker compose logs nginx backend1 backend2`) — causas que surgiram aqui:
	- Dependência Python ausente em `backend/requirements.txt` (ex.: `Flask-SQLAlchemy`) — solução: adicionar e rebuildar imagens.
	- Erro de inicialização do Flask por mudanças de API (Flask 3 removeu `before_first_request` como decorador direto) — solução aplicada: usar fallback `before_request` com execução única para `db.create_all()`.
	- Backends não prontos antes do proxy encaminhar — adicione healthchecks no `docker-compose.yml` e/ou um entrypoint que aguarde a DB.

**Notas para PR / CI**

- Próximo passo recomendado: adicionar workflow GitHub Actions que mostre `docker compose build` e smoke tests (ou use runners com Docker-in-Docker). Incluir checagens de lint e testes unitários quando disponíveis.
- Para abrir PR: branch `feature/docker-compose` contém a scaffold; abra PR com descrição das mudanças, imagens geradas e instruções de teste local (este README).

Se quiser, eu posso adicionar o workflow de CI e um template de PR automaticamente.
