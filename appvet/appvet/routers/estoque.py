"""Rotas de estoque e medicamentos."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from appvet import models, schemas
from appvet.database import get_db

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.get("/", response_model=list[schemas.EstoqueItem])
def listar_itens(db: Session = Depends(get_db)):
    return db.query(models.EstoqueItem).all()


@router.post("/", response_model=schemas.EstoqueItem, status_code=201)
def criar_item(item: schemas.EstoqueItemCreate, db: Session = Depends(get_db)):
    novo = models.EstoqueItem(**item.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.patch("/{item_id}/baixa", response_model=schemas.EstoqueItem)
def dar_baixa(item_id: int, quantidade: int = Query(default=1, gt=0), db: Session = Depends(get_db)):
    """Dá baixa em uma quantidade do item, por exemplo ao usar em um atendimento."""
    item = db.get(models.EstoqueItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    if item.quantidade < quantidade:
        raise HTTPException(status_code=400, detail="Quantidade em estoque insuficiente")
    item.quantidade -= quantidade
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
def excluir_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(models.EstoqueItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(item)
    db.commit()
