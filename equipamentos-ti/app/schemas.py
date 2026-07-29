"""Schemas Pydantic (entrada/saída da API)."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from app.models import StatusEquipamento, TipoEquipamento


class HistoricoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: datetime
    acao: str
    detalhe: str


class EquipamentoBase(BaseModel):
    tipo: TipoEquipamento = TipoEquipamento.CELULAR
    status: StatusEquipamento = StatusEquipamento.ESTOQUE
    marca: str
    modelo: str
    serie: str
    operadora: str | None = None
    linha: str | None = None
    imei1: str | None = None
    imei2: str | None = None
    identidade: str | None = None
    cpf: str | None = None
    responsavel: str | None = None
    data_aquisicao: date
    valor: float
    observacao: str | None = None


class EquipamentoCreate(EquipamentoBase):
    pass


class EquipamentoUpdate(BaseModel):
    tipo: TipoEquipamento
    status: StatusEquipamento
    marca: str
    modelo: str
    serie: str
    operadora: str | None = None
    linha: str | None = None
    imei1: str | None = None
    imei2: str | None = None
    identidade: str
    cpf: str
    responsavel: str
    data_aquisicao: date
    valor: float
    observacao: str | None = None


class Movimentacao(BaseModel):
    responsavel: str | None = None
    status: StatusEquipamento
    nota: str | None = None


class EquipamentoOut(EquipamentoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tag: str
    criado_em: datetime


class EquipamentoDetalheOut(EquipamentoOut):
    historico: list[HistoricoOut] = []


class Estatisticas(BaseModel):
    total: int
    em_uso: int
    manutencao: int
    estoque: int
