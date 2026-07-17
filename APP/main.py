from fastapi import FastAPI, Depends    #import FastAPI e Depends do módulo fastapi. FastAPI é a classe principal para criar a aplicação web, enquanto Depends é usado para declarar dependências em rotas.
from sqlalchemy.orm import Session      #Importa a classe Session do módulo sqlalchemy.orm. Session é usada para interagir com o banco de dados, permitindo consultas e operações de persistência.
from app import models, schemas     # pega a class que foi definido em models.py
from app.database import Base, engine, get_db   # Importa a classe do database.py para o arquivo main.py
from fastapi import HTTPException

app = FastAPI(title="My API")   #aplicando um titulo para a aplicação FastAPI

@app.get("/vagas", response_model=list[schemas.Vaga])   # pega os dados colocando em um modelo de lista de vagas, que é definido em schemas.py 
def read_vagas(db: Session = Depends(get_db)):  # funçao que lê as vagas do banco de dados, usando a sessão do SQLAlchemy como dependência e abrindo e fechando a conexão com o banco de dados automaticamente.
    vagas = db.query(models.Vaga).all()   # Consulta todas as vagas no banco de dados usando a sessão do SQLAlchemy.
    return vagas    # Retorna a lista de vagas como resposta da API. 
    
@app.get("/vagas/{vaga_id}", response_model=schemas.Vaga)   # pega os dados testanto uma vaga para ver se tem id, que foi definido em schemas.py 
def read_vaga(vaga_id: int, db: Session = Depends(get_db)):  # funçao que lê as vaga do banco de dados, usando a sessão do SQLAlchemy como dependência e abrindo e fechando a conexão com o banco de dados automaticamente.
    vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()   # Filtra a consulta para encontrar a vaga com o ID especificado. Se não for encontrada, retorna None.
    if not vaga:    # Se a vaga não for encontrada, levanta uma exceção HTTP com status 404 e uma mensagem de erro.
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return vaga    # Retorna a vaga como resposta da API. 

Base.metadata.create_all(bind=engine)   #Cria as tabelas no banco de dados de acordo com os modelos definidos no SQLAlchemy. Isso garante que todas as tabelas necessárias sejam criadas antes de qualquer operação de banco de dados ser realizada. 

@app.post("/vagas", response_model=schemas.Vaga)    # Define uma rota POST para criar uma nova vaga. A resposta será um objeto do modelo schemas.Vaga.
def create_vaga(vaga: schemas.VagaBase, db: Session = Depends(get_db)):  # Função que cria uma nova vaga no banco de dados. Recebe os dados da vaga como um objeto schemas.VagaBase e a sessão do SQLAlchemy como dependência.
    db_vaga = models.Vaga(**vaga.model_dump())   # Cria uma instância do modelo Vaga usando os dados fornecidos. O método dict() converte o objeto Pydantic em um dicionário.
    db.add(db_vaga)   # Adiciona a nova vaga à sessão do SQLAlchemy.
    db.commit()   # Confirma a transação, salvando a nova vaga no banco de dados.
    db.refresh(db_vaga)   # Atualiza a instância db_vaga com os dados mais recentes do banco de dados, incluindo o ID gerado automaticamente.
    return db_vaga   # Retorna a nova vaga como resposta da API.

@app.put("/vagas/{vaga_id}", response_model=schemas.Vaga)   # Define uma rota PUT para atualizar uma vaga existente. A resposta será um objeto do modelo schemas.Vaga.
def update_vaga(vaga_id: int, vaga: schemas.VagaBase, db: Session = Depends(get_db)):  # Função que atualiza uma vaga existente no banco de dados. Recebe o ID da vaga, os novos dados como um objeto schemas.VagaBase e a sessão do SQLAlchemy como dependência.
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()   # Consulta a vaga existente no banco de dados pelo ID.
    if not db_vaga:   # Se a vaga não for encontrada, levanta uma exceção HTTP com status 404 e uma mensagem de erro.
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    for key, value in vaga.model_dump().items():   # Atualiza os atributos da vaga existente com os novos valores fornecidos.
        setattr(db_vaga, key, value)
    db.commit()   # Confirma a transação, salvando as alterações no banco de dados.
    db.refresh(db_vaga)   # Atualiza a instância db_vaga com os dados mais recentes do banco de dados.
    return db_vaga   # Retorna a vaga atualizada como resposta da API.
    
@app.delete("/vagas/{vaga_id}", response_model=schemas.Vaga)   # Define uma rota DELETE para remover uma vaga existente. A resposta será um objeto do modelo schemas.Vaga.
def delete_vaga(vaga_id: int, db: Session = Depends(get_db)): # Função que remove uma vaga existente do banco de dados. Recebe o ID da vaga e a sessão do SQLAlchemy como dependência.
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()   # Consulta a vaga existente no banco de dados pelo ID.
    if not db_vaga:   # Se a vaga não for encontrada, levanta uma exceção HTTP com status 404 e uma mensagem de erro.
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    db.delete(db_vaga)   # Remove a vaga da sessão do SQLAlchemy.
    db.commit()   # Confirma a transação, removendo a vaga do banco de dados.
    return db_vaga   # Retorna a vaga removida como resposta da API.
