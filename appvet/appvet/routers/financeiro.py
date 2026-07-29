"""Rotas do módulo financeiro."""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Literal
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])


@router.get("/", response_model=list[schemas.LancamentoFinanceiro])
def listar_lancamentos(db: Session = Depends(get_db)):
    return (
        db.query(models.LancamentoFinanceiro)
        .order_by(models.LancamentoFinanceiro.data.desc())
        .all()
    )


@router.post("/", response_model=schemas.LancamentoFinanceiro, status_code=201)
def criar_lancamento(lancamento: schemas.LancamentoFinanceiroCreate, db: Session = Depends(get_db)):
    novo = models.LancamentoFinanceiro(**lancamento.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.patch("/{lancamento_id}/status", response_model=schemas.LancamentoFinanceiro)
def atualizar_status(
    lancamento_id: int,
    status: Literal["Pago", "Pendente"] = Query(),
    db: Session = Depends(get_db),
):
    lancamento = db.get(models.LancamentoFinanceiro, lancamento_id)
    if not lancamento:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    lancamento.status = status
    db.commit()
    db.refresh(lancamento)
    return lancamento


@router.get("/resumo/totais")
def resumo_totais(db: Session = Depends(get_db)):
    lancamentos = (
        db.query(models.LancamentoFinanceiro)
        .filter(models.LancamentoFinanceiro.status == "Pago")
        .all()
    )
    receitas = sum(item.valor for item in lancamentos if item.tipo == "Receita")
    despesas = sum(item.valor for item in lancamentos if item.tipo == "Despesa")
    return {"receitas": receitas, "despesas": despesas, "saldo": receitas - despesas}
