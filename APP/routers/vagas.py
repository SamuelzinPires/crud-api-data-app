from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/vagas", tags=["vagas"])  # prefix soma "/vagas" na frente de toda rota daqui; tags só agrupa no /docs


@router.get("", response_model=list[schemas.Vaga])  # "" aqui vira "/vagas" por causa do prefix
def read_vagas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):  # skip/limit vêm da query string (?skip=...&limit=...), com padrão pra quando ninguém manda nada
    vagas = db.query(models.Vaga).offset(skip).limit(limit).all()  # pula "skip" registros, pega até "limit" - é a paginação
    return vagas  # lista vazia é resposta válida (200), não é erro


@router.get("/{vaga_id}", response_model=schemas.Vaga)  # "/{vaga_id}" vira "/vagas/{vaga_id}"; {vaga_id} é parte da URL, não query string
def read_vaga(vaga_id: int, db: Session = Depends(get_db)):
    vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()  # .first() -> None se não achar nenhuma
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")  # 404 = recurso não existe (convenção REST)
    return vaga


@router.post("", response_model=schemas.Vaga, status_code=201)  # 201 = "recurso criado" - não é automático, precisa declarar
def create_vaga(vaga: schemas.VagaBase, db: Session = Depends(get_db)):  # VagaBase = schema de entrada, sem id (o banco gera)
    db_vaga = models.Vaga(**vaga.model_dump())  # .model_dump() vira dict; ** desempacota como argumentos nomeados do model
    db.add(db_vaga)      # marca pra inserir
    db.commit()          # de fato salva no banco
    db.refresh(db_vaga)  # busca de volta os dados atualizados (principalmente o id, gerado pelo banco)
    return db_vaga


@router.put("/{vaga_id}", response_model=schemas.Vaga)
def update_vaga(vaga_id: int, vaga: schemas.VagaBase, db: Session = Depends(get_db)):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    for key, value in vaga.model_dump().items():  # percorre os 5 campos recebidos
        setattr(db_vaga, key, value)               # e aplica cada um na vaga já existente no banco
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.delete("/{vaga_id}", response_model=schemas.Vaga)
def delete_vaga(vaga_id: int, db: Session = Depends(get_db)):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    db.delete(db_vaga)   # marca pra remover
    db.commit()           # de fato remove do banco
    return db_vaga        # retorna o que foi apagado, útil pra quem chamou confirmar o que sumiu