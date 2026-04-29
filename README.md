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
