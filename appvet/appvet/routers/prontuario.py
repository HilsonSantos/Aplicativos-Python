"""Rotas de prontuário eletrônico."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/prontuario", tags=["Prontuário"])


@router.get("/{paciente_id}", response_model=list[schemas.ProntuarioEntrada])
def listar_entradas(paciente_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.ProntuarioEntrada)
        .filter(models.ProntuarioEntrada.paciente_id == paciente_id)
        .order_by(models.ProntuarioEntrada.data.desc())
        .all()
    )


@router.post("/", response_model=schemas.ProntuarioEntrada, status_code=201)
def criar_entrada(entrada: schemas.ProntuarioEntradaCreate, db: Session = Depends(get_db)):
    if not db.get(models.Paciente, entrada.paciente_id):
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    nova = models.ProntuarioEntrada(**entrada.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova
