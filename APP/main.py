from fastapi import FastAPI   # FastAPI é a classe principal para criar a aplicação web.
from app.database import Base, engine   # engine/Base usados só aqui pra criar as tabelas na subida da API.
from app.routers import vagas   # router com as rotas de /vagas, movidas pra app/routers/vagas.py

app = FastAPI(title="My API")   # aplicando um titulo para a aplicação FastAPI


@app.on_event("startup")   # só roda quando a API sobe de verdade (uvicorn/fastapi dev) - não quando o módulo é só importado (ex: pelos testes)
def criar_tabelas():
    Base.metadata.create_all(bind=engine)   # Cria as tabelas no banco de dados de acordo com os modelos definidos no SQLAlchemy.


app.include_router(vagas.router)   # registra todas as rotas de /vagas nesse app
