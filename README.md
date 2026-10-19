# TaskFlow

API REST para gerenciamento de projetos, tarefas e usuários, organizada em
camadas de domínio, casos de uso, repositórios SQLAlchemy e transporte FastAPI.

## Requisitos

- Python 3.12 ou superior
- PostgreSQL 16 (ou SQLite para execução dos testes)

O driver configurado para PostgreSQL é `psycopg` 3, incluído como
`psycopg[binary]` em `requirements.txt`.

## Execução local

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Altere `POSTGRES_PASSWORD` e a senha correspondente em `POSTGRESQL_URL` no
arquivo `.env`, depois inicie a API:

```sh
uvicorn FastAPI.main:app --reload
```

Na inicialização, a aplicação conecta ao banco, importa os modelos e cria as
tabelas ausentes. A documentação interativa fica em
[http://localhost:8000/docs](http://localhost:8000/docs); o esquema OpenAPI está
em [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json).

## Dashboard web

O dashboard React/TypeScript fica em `frontend/` e consome os endpoints existentes
de projetos e tarefas. Inicie a API conforme as instruções acima e, em outro
terminal, execute:

```sh
cd frontend
pnpm install
cp .env.example .env.local
pnpm dev
```

O Vite encaminha `/api` para `http://localhost:8000` por padrão, sem exigir CORS
no desenvolvimento local. Para mudar o endereço, ajuste `TASKFLOW_API_TARGET`
em `frontend/.env.local`; `VITE_API_BASE_URL` pode apontar diretamente para uma
URL-base permitida por CORS. Gere os arquivos estáticos com `cd frontend && pnpm
build`; a saída fica em `frontend/dist/`.

## Execução com Docker Compose

Copie `.env.example` para `.env`, defina uma senha local e execute:

```sh
docker compose up --build
```

O Compose aguarda o PostgreSQL ficar saudável antes de iniciar a API. A
persistência do banco usa o volume `postgres_data`.

## Rotas

- `GET`, `POST`, `GET /{id}`, `PATCH /{id}` e `DELETE /{id}` em `/projetos`
- `POST`, `GET /{id}`, `PATCH /{id}` e `DELETE /{id}` em `/tarefas`
- `GET /tarefas?projeto_id={id}` lista as tarefas de um projeto
- `POST /usuarios` cria usuários; `GET /usuarios/{email}` busca pelo e-mail

Projetos com tarefas não podem ser excluídos. Tarefas referenciam projetos
existentes. O endpoint de criação de usuário valida e-mail e trata duplicatas
com `409`; as respostas públicas nunca incluem senha ou hash. Autenticação não
faz parte do escopo desta versão.

## Testes

```sh
pytest
```

Os testes usam SQLite em memória, inicializado pelo mesmo fluxo de criação do
schema da aplicação, sem exigir PostgreSQL.
