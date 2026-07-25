# CRUD API Data Application — Vagas

CRUD completo construído do zero com **FastAPI** + **PostgreSQL**, com uma interface em **Streamlit** por cima, para gerenciar vagas de emprego. Projeto pessoal de aprendizado (primeiro CRUD "real" do autor), pensado também como ferramenta de uso diário — substitui uma lista manual de vagas por um app com API de verdade por trás.

Os dados iniciais vêm de um projeto separado de scraping, o **ETL Vagas Tech**, que extrai vagas reais de portais de emprego e gera um CSV — esta API só consome esse resultado, não faz scraping.

## Funcionalidades

**API (FastAPI + PostgreSQL)**
- CRUD completo de vagas (criar, listar, buscar por id, atualizar, excluir)
- Paginação (`skip`/`limit`) na listagem
- Validação de dados com Pydantic (campos obrigatórios não podem ser vazios)
- Documentação automática interativa (Swagger UI em `/docs`)

**Interface (Streamlit)**
- Listagem paginada de vagas, com filtro por nível
- Cadastro, edição e exclusão de vagas direto pela interface (barra lateral)
- Tratamento de erro de conexão com a API

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) — API REST
- [PostgreSQL](https://www.postgresql.org/) — banco de dados
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [Docker Compose](https://docs.docker.com/compose/) — sobe o banco de dados
- [Streamlit](https://streamlit.io/) — interface web
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente

## Estrutura do projeto

```
crud-api-fastapi/
├── app/
│   ├── main.py              # cria a aplicação FastAPI e inclui as rotas
│   ├── database.py          # engine, SessionLocal, Base, get_db()
│   ├── models.py            # model SQLAlchemy (Vaga)
│   ├── schemas.py           # schemas Pydantic (VagaBase, Vaga)
│   └── routers/
│       └── vagas.py         # rotas de /vagas (GET, POST, PUT, DELETE)
├── data/
│   └── vagas_limpas.csv     # dado real, gerado pelo scraper ETL Vagas Tech (versionado - já vem pronto pra importar)
├── streamlit_app.py         # interface web
├── seed_data.py             # importa o CSV pra API (POST linha a linha)
├── docker-compose.yml       # container do Postgres
├── requirements.txt
└── .env                     # credenciais do banco (não versionado)
```

## Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Docker Desktop

### 1. Clonar e instalar dependências
```bash
git clone <url-do-repositorio>
cd crud-api-fastapi
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
Cria um arquivo `.env` na raiz do projeto:
```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=crud_api
DB_HOST=localhost
DB_PORT=5432
```

### 3. Subir o banco de dados
```bash
docker compose up -d
```

### 4. Rodar a API
```bash
fastapi dev app/main.py
```
A tabela `vagas` é criada automaticamente na primeira subida. A API fica em `http://127.0.0.1:8000`, com documentação interativa em `http://127.0.0.1:8000/docs`.

### 5. (Opcional) Importar dados reais
O repositório já vem com `data/vagas_limpas.csv` (dado real do scraper ETL Vagas Tech). Com a API rodando, num terminal separado:
```bash
python seed_data.py
```
Lê o CSV e cadastra cada vaga via `POST /vagas` — sem precisar de nenhum arquivo externo, funciona direto após o clone.

### 6. Rodar a interface
Em outro terminal (API e Docker já ativos):
```bash
streamlit run streamlit_app.py
```

## Endpoints da API

| Método | Rota | Descrição | Sucesso |
|---|---|---|---|
| GET | `/vagas?skip=0&limit=10` | Lista vagas (paginado) | `200` |
| GET | `/vagas/{id}` | Busca uma vaga pelo id | `200` / `404` |
| POST | `/vagas` | Cria uma vaga | `201` |
| PUT | `/vagas/{id}` | Atualiza uma vaga | `200` / `404` |
| DELETE | `/vagas/{id}` | Remove uma vaga | `200` / `404` |

**Campos da vaga:** `titulo`, `empresa` e `link` são obrigatórios; `formato` e `nivel` são opcionais (nem toda vaga raspada tem essa informação).

## Roadmap (v2)

Fora do escopo desta primeira versão, documentado aqui como próximos passos:
- Campo `status` de candidatura (acompanhamento pessoal: "quero aplicar", "aplicado", "entrevista"...)
- Streamlit em 2 abas: vagas disponíveis → selecionar → vira candidatura acompanhada
- Paginação/filtro por nível resolvidos no backend (hoje o filtro por nível é aplicado no lado do Streamlit, só sobre a página já carregada)

## Autor

Desenvolvido por Samuel Pires, como parte de uma trilha de aprendizado em Engenharia de Dados.