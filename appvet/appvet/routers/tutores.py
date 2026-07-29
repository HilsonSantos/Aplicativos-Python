"""Rotas de tutores e pacientes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/tutores", tags=["Tutores e pacientes"])


@router.get("/", response_model=list[schemas.Tutor])
def listar_tutores(db: Session = Depends(get_db)):
    return db.query(models.Tutor).all()


@router.post("/", response_model=schemas.Tutor, status_code=201)
def criar_tutor(tutor: schemas.TutorCreate, db: Session = Depends(get_db)):
    novo = models.Tutor(**tutor.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/{tutor_id}", response_model=schemas.Tutor)
def obter_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.get(models.Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return tutor


@router.delete("/{tutor_id}", status_code=204)
def excluir_tutor(tutor_id: int, db: Session = Depends(get_db)):
    tutor = db.get(models.Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    paciente_ids = [paciente.id for paciente in tutor.pacientes]
    possui_registros = paciente_ids and any(
        db.query(modelo).filter(modelo.paciente_id.in_(paciente_ids)).first()
        for modelo in (models.Agendamento, models.ProntuarioEntrada, models.Internacao)
    )
    if possui_registros:
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir tutor com histórico clínico, agenda ou internação.",
        )
    db.delete(tutor)
    db.commit()


@router.post("/{tutor_id}/pacientes", response_model=schemas.Paciente, status_code=201)
def criar_paciente(tutor_id: int, paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    tutor = db.get(models.Tutor, tutor_id)
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    novo = models.Paciente(tutor_id=tutor_id, **paciente.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/pacientes/todos", response_model=list[schemas.Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()
