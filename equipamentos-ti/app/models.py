"""Modelos de dados (SQLAlchemy ORM)."""

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TipoEquipamento(str, enum.Enum):
    CELULAR = "celular"
    COMPUTADOR = "computador"
    NOTEBOOK = "notebook"
    IMPRESSORA = "impressora"
    ROTEADOR = "roteador"


class StatusEquipamento(str, enum.Enum):
    EM_USO = "em_uso"
    MANUTENCAO = "manutencao"
    ESTOQUE = "estoque"
    DESCARTE = "descarte"


def _gerar_tag(tipo: str) -> str:
    prefixos = {
        "celular": "CEL",
        "computador": "CPU",
        "notebook": "NTB",
        "impressora": "IMP",
        "roteador": "ROT",
    }
    prefixo = prefixos.get(tipo, "EQP")
    return f"{prefixo}-{uuid.uuid4().hex[:5].upper()}"


class Equipamento(Base):
    __tablename__ = "equipamentos"

    # CAMPOS GERAIS #
    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    tipo: Mapped[TipoEquipamento] = mapped_column(
        Enum(TipoEquipamento),
        default=TipoEquipamento.CELULAR,
        nullable=False,
    )
    status: Mapped[StatusEquipamento] = mapped_column(
        Enum(StatusEquipamento),
        default=StatusEquipamento.EM_USO,
        nullable=False,
    )
    marca: Mapped[str] = mapped_column(String(100), nullable=False)
    modelo: Mapped[str] = mapped_column(String(100), nullable=False)
    serie: Mapped[str] = mapped_column(String(100), nullable=False)
    observacao: Mapped[str] = mapped_column(Text, nullable=True)
    data_aquisicao: Mapped[date] = mapped_column(Date, nullable=True)
    valor: Mapped[float] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    historico: Mapped[list["HistoricoMovimentacao"]] = relationship(
        back_populates="equipamento",
        cascade="all, delete-orphan",
        order_by="HistoricoMovimentacao.data.asc()",
    )

    # QUANDO FOR APARELHO CELULAR #
    operadora: Mapped[str] = mapped_column(String(10), nullable=True)
    linha: Mapped[str] = mapped_column(String(11), nullable=True)
    imei1: Mapped[str] = mapped_column(String(15), nullable=True)
    imei2: Mapped[str] = mapped_column(String(15), nullable=True)

    # QUANDO FOR APARELHO CELULAR E NOTEBOOK #
    identidade: Mapped[str] = mapped_column(String(10), nullable=True)
    cpf: Mapped[str] = mapped_column(String(11), nullable=True)
    responsavel: Mapped[str] = mapped_column(String(120), nullable=True)

    def gerar_tag_se_vazia(self) -> None:
        if not self.tag:
            tipo = self.tipo.value \
                if isinstance(self.tipo, TipoEquipamento) else self.tipo
            self.tag = _gerar_tag(tipo)


class HistoricoMovimentacao(Base):
    __tablename__ = "historico_movimentacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    equipamento_id: Mapped[int] = mapped_column(ForeignKey("equipamentos.id"))
    data: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    acao: Mapped[str] = mapped_column(String(60))
    detalhe: Mapped[str] = mapped_column(Text)

    equipamento: Mapped["Equipamento"] = relationship(back_populates="historico")
