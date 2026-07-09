from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Url_banco = "postgresql://Admin:Admin123@localhost:5432/FastAPI_DB"

engine = create_engine(Url_banco) #pool de conexões com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  #Janelas de atendimento
Base = declarative_base() 

def get_db():
    db = SessionLocal()  #passando os parametros de configuração do banco de dados para a variável db
    try:
        yield db    #return, Falando com o banco de dados
    finally:
        db.close()   #fecha a conexão com o banco de dados
     