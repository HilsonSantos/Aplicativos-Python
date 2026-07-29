"""Rotas de internação veterinária."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/internacao", tags=["Internação"])


@router.get("/", response_model=list[schemas.Internacao])
def listar_internacoes(apenas_ativas: bool = True, db: Session = Depends(get_db)):
    query = db.query(models.Internacao)
    if apenas_ativas:
        query = query.filter(models.Internacao.ativa.is_(True))
    return query.all()


@router.post("/", response_model=schemas.Internacao, status_code=201)
def criar_internacao(internacao: schemas.InternacaoCreate, db: Session = Depends(get_db)):
    if not db.get(models.Paciente, internacao.paciente_id):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    nova = models.Internacao(**internacao.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.post("/{internacao_id}/alta", response_model=schemas.Internacao)
def registrar_alta(internacao_id: int, db: Session = Depends(get_db)):
    internacao = db.get(models.Internacao, internacao_id)
    if not internacao:
        raise HTTPException(status_code=404, detail="Internação não encontrada")
    internacao.ativa = False
    db.commit()
    db.refresh(internacao)
    return internacao
