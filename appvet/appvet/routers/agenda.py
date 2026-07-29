"""Rotas de agenda e agendamentos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/agenda", tags=["Agenda"])


@router.get("/", response_model=list[schemas.Agendamento])
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(models.Agendamento).order_by(models.Agendamento.data_hora).all()


@router.post("/", response_model=schemas.Agendamento, status_code=201)
def criar_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    if not db.get(models.Paciente, agendamento.paciente_id):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    novo = models.Agendamento(**agendamento.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.patch("/{agendamento_id}/status", response_model=schemas.Agendamento)
def atualizar_status(
    agendamento_id: int, payload: schemas.AgendamentoStatusUpdate, db: Session = Depends(get_db)
):
    agendamento = db.get(models.Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    agendamento.status = payload.status
    db.commit()
    db.refresh(agendamento)
    return agendamento


@router.delete("/{agendamento_id}", status_code=204)
def excluir_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.get(models.Agendamento, agendamento_id)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    db.delete(agendamento)
    db.commit()
