"""API FastAPI para controle de equipamentos de TI."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db, init_db
from app.models import StatusEquipamento, TipoEquipamento
from app.schemas import (
    EquipamentoCreate,
    EquipamentoDetalheOut,
    EquipamentoOut,
    EquipamentoUpdate,
    Estatisticas,
    Movimentacao,
)

app = FastAPI(
    title="Controle de Equipamentos de TI",
    description=(
        "API para cadastro, empréstimo e histórico de equipamentos "
        "(celulares, CPUs, notebooks)."
    ),
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


def _buscar_ou_404(db: Session, equipamento_id: int):
    equipamento = crud.obter_equipamento(db, equipamento_id)
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado.")
    return equipamento


@app.get("/equipamentos", response_model=list[EquipamentoOut])
def listar_equipamentos(
    tipo: TipoEquipamento | None = None,
    status: StatusEquipamento | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.listar_equipamentos(db, tipo=tipo, status=status, q=q)


@app.post("/equipamentos", response_model=EquipamentoOut, status_code=201)
def criar_equipamento(dados: EquipamentoCreate, db: Session = Depends(get_db)):
    return crud.criar_equipamento(db, dados)


@app.get("/equipamentos/estatisticas", response_model=Estatisticas)
def obter_estatisticas(db: Session = Depends(get_db)):
    return crud.estatisticas(db)


@app.get("/equipamentos/{equipamento_id}", response_model=EquipamentoDetalheOut)
def obter_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    return _buscar_ou_404(db, equipamento_id)


@app.put("/equipamentos/{equipamento_id}", response_model=EquipamentoOut)
def atualizar_equipamento(
    equipamento_id: int, dados: EquipamentoUpdate, db: Session = Depends(get_db)
):
    equipamento = _buscar_ou_404(db, equipamento_id)
    return crud.atualizar_equipamento(db, equipamento, dados)


@app.post("/equipamentos/{equipamento_id}/movimentar", response_model=EquipamentoOut)
def movimentar_equipamento(
    equipamento_id: int, dados: Movimentacao, db: Session = Depends(get_db)
):
    equipamento = _buscar_ou_404(db, equipamento_id)
    return crud.movimentar_equipamento(db, equipamento, dados)


@app.delete("/equipamentos/{equipamento_id}", status_code=204)
def excluir_equipamento(equipamento_id: int, db: Session = Depends(get_db)):
    equipamento = _buscar_ou_404(db, equipamento_id)
    crud.excluir_equipamento(db, equipamento)
