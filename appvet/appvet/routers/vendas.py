"""Rotas de vendas e frente de caixa."""

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/vendas", tags=["Vendas e caixa"])


@router.get("/", response_model=list[schemas.Venda])
def listar_vendas(db: Session = Depends(get_db)):
    return db.query(models.Venda).order_by(models.Venda.data.desc()).all()


@router.post("/", response_model=schemas.Venda, status_code=201)
def finalizar_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    total = sum(item.preco * item.quantidade for item in venda.itens)
    descricao = ", ".join(f"{item.quantidade}x {item.nome}" for item in venda.itens)

    nova_venda = models.Venda(data=datetime.utcnow(), total=total, itens_descricao=descricao)
    db.add(nova_venda)

    lancamento = models.LancamentoFinanceiro(
        data=datetime.utcnow(),
        descricao=f"Venda no caixa ({len(venda.itens)} item(ns))",
        tipo="Receita",
        valor=total,
        status="Pago",
    )
    db.add(lancamento)

    db.commit()
    db.refresh(nova_venda)
    return nova_venda
