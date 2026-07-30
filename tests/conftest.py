import pytest 
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

engine = create_engine("sqlite:///./test.db") 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db    #return, Falando com o banco de dados
    finally:
        db.close()   #fecha a conexão com o banco de dados   
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture 
def client():
    Base.metadata.create_all(bind=engine) # Cria um banco para o teste
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)  # Drop do banco de testes 