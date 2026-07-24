from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/vagas", tags=["vagas"])


@router.get("", response_model=list[schemas.Vaga])
def read_vagas(skip:int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vagas = db.query(models.Vaga).offset(skip).limit(limit).all()
    return vagas


@router.get("/{vaga_id}", response_model=schemas.Vaga)
def read_vaga(vaga_id: int, db: Session = Depends(get_db)):
    vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return vaga


@router.post("", response_model=schemas.Vaga, status_code=201)
def create_vaga(vaga: schemas.VagaBase, db: Session = Depends(get_db)):
    db_vaga = models.Vaga(**vaga.model_dump())
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.put("/{vaga_id}", response_model=schemas.Vaga)
def update_vaga(vaga_id: int, vaga: schemas.VagaBase, db: Session = Depends(get_db)):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    for key, value in vaga.model_dump().items():
        setattr(db_vaga, key, value)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.delete("/{vaga_id}", response_model=schemas.Vaga)
def delete_vaga(vaga_id: int, db: Session = Depends(get_db)):
    db_vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not db_vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    db.delete(db_vaga)
    db.commit()
    return db_vaga
