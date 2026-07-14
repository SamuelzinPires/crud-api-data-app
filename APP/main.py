from fastapi import FastAPI # conexão com a FastApi
from app import models # pega a class que foi definido em models.py 
from app.database import Base, engine # Importa a classe do database.py para o arquivo main.py

app = FastAPI(title="My API")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

Base.metadata.create_all(bind=engine) #Cria as tabelas no banco de dados de acordo com os modelos definidos no SQLAlchemy. Isso garante que todas as tabelas necessárias sejam criadas antes de qualquer operação de banco de dados ser realizada.