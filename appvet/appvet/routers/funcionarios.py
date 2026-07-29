"""Rotas de funcionários e prestadores."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


@router.get("/", response_model=list[schemas.Funcionario])
def listar_funcionarios(db: Session = Depends(get_db)):
    return db.query(models.Funcionario).all()


@router.post("/", response_model=schemas.Funcionario, status_code=201)
def criar_funcionario(funcionario: schemas.FuncionarioCreate, db: Session = Depends(get_db)):
    novo = models.Funcionario(**funcionario.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo
