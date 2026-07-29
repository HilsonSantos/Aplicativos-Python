"""Operações de banco de dados para equipamentos e histórico."""

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import (
    Equipamento,
    HistoricoMovimentacao,
    StatusEquipamento,
    TipoEquipamento,
)
from app.schemas import EquipamentoCreate, EquipamentoUpdate, Movimentacao

STATUS_LABELS = {
    StatusEquipamento.EM_USO: "Em uso",
    StatusEquipamento.MANUTENCAO: "Manutenção",
    StatusEquipamento.ESTOQUE: "Estoque",
}


def listar_equipamentos(
    db: Session,
    tipo: TipoEquipamento | None = None,
    status: StatusEquipamento | None = None,
    q: str | None = None,
) -> list[Equipamento]:
    stmt = select(Equipamento)

    if tipo:
        stmt = stmt.where(Equipamento.tipo == tipo)

    if status:
        stmt = stmt.where(Equipamento.status == status)

    if q:
        termo = f"%{q.strip().lower()}%"
        stmt = stmt.where(
            or_(
                func.lower(Equipamento.tag).like(termo),
                func.lower(Equipamento.modelo).like(termo),
                func.lower(Equipamento.responsavel).like(termo),
            )
        )
    return list(db.execute(stmt).scalars().all())


def obter_equipamento(db: Session, equipamento_id: int) -> Equipamento | None:
    return db.get(Equipamento, equipamento_id)


def criar_equipamento(db: Session, dados: EquipamentoCreate) -> Equipamento:
    equipamento = Equipamento(**dados.model_dump())
    equipamento.gerar_tag_se_vazia()
    db.add(equipamento)
    db.flush()

    detalhe = f"Equipamento cadastrado como {STATUS_LABELS[equipamento.status].lower()}"
    if equipamento.responsavel:
        detalhe += f", sob responsabilidade de {equipamento.responsavel}"
    db.add(
        HistoricoMovimentacao(
            equipamento_id=equipamento.id,
            acao="Cadastro",
            detalhe=detalhe + ".",
        )
    )
    db.commit()
    db.refresh(equipamento)
    return equipamento


def atualizar_equipamento(
    db: Session, equipamento: Equipamento, dados: EquipamentoUpdate
) -> Equipamento:
    alteracoes = dados.model_dump(exclude_unset=True)
    for campo, valor in alteracoes.items():
        setattr(equipamento, campo, valor)
    if alteracoes:
        db.add(
            HistoricoMovimentacao(
                equipamento_id=equipamento.id,
                acao="Edição",
                detalhe="Dados do equipamento atualizados.",
            )
        )
    db.commit()
    db.refresh(equipamento)
    return equipamento


def movimentar_equipamento(
    db: Session, equipamento: Equipamento, dados: Movimentacao
) -> Equipamento:
    de = equipamento.responsavel or "estoque"
    para = dados.responsavel or "estoque"

    if de != para:
        detalhe = (
            f"Movimentado de {de} para {para}. "
            f"Status: {STATUS_LABELS[dados.status]}."
        )
    else:
        detalhe = f"Status alterado para {STATUS_LABELS[dados.status]}."
    if dados.nota:
        detalhe += f" Obs: {dados.nota}"

    equipamento.responsavel = dados.responsavel
    equipamento.status = dados.status
    db.add(
        HistoricoMovimentacao(
            equipamento_id=equipamento.id,
            acao="Movimentação",
            detalhe=detalhe,
        )
    )
    db.commit()
    db.refresh(equipamento)
    return equipamento


def excluir_equipamento(db: Session, equipamento: Equipamento) -> None:
    db.delete(equipamento)
    db.commit()


def estatisticas(db: Session) -> dict[str, int]:
    equipamentos = db.execute(select(Equipamento)).scalars().all()
    return {
        "total": len(equipamentos),
        "em_uso": sum(1 for e in equipamentos if e.status == StatusEquipamento.EM_USO),
        "manutencao": sum(1 for e in equipamentos if e.status == StatusEquipamento.MANUTENCAO),
        "estoque": sum(1 for e in equipamentos if e.status == StatusEquipamento.ESTOQUE),
    }
