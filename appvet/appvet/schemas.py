"""Schemas Pydantic usados pela API (entrada e saída)."""

from datetime import datetime

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PacienteBase(BaseModel):
    nome: str
    especie: str = ""
    raca: str = ""
    sexo: str = ""
    idade: str = ""
    peso: str = ""
    pelagem: str = ""
    microchip: str = ""
    alergias: str = ""
    doencas: str = ""
    medicamentos: str = ""
    vacinas: str = ""


class PacienteCreate(PacienteBase):
    pass


class Paciente(PacienteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tutor_id: int


class TutorBase(BaseModel):
    nome: str
    telefone: str = ""
    email: str = ""
    endereco: str = ""
    documento: str = ""


class TutorCreate(TutorBase):
    pass


class Tutor(TutorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    pacientes: list[Paciente] = []


class AgendamentoBase(BaseModel):
    paciente_id: int
    data_hora: datetime
    tipo: str = "Consulta"
    veterinario: str = ""
    status: Literal["Aguardando", "Confirmado", "Encaixe", "Atendido", "Falta"] = "Aguardando"


class AgendamentoCreate(AgendamentoBase):
    pass


class Agendamento(AgendamentoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AgendamentoStatusUpdate(BaseModel):
    status: Literal["Aguardando", "Confirmado", "Encaixe", "Atendido", "Falta"]


class ProntuarioEntradaBase(BaseModel):
    paciente_id: int
    veterinario: str = ""
    queixa: str = ""
    exame: str = ""
    diagnostico: str = ""
    prescricao: str = ""
    peso: str = ""
    temperatura: str = ""


class ProntuarioEntradaCreate(ProntuarioEntradaBase):
    pass


class ProntuarioEntrada(ProntuarioEntradaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data: datetime


class InternacaoBase(BaseModel):
    paciente_id: int
    leito: str = ""
    veterinario: str = ""
    diagnostico: str = ""
    previsao_alta: str = ""
    fluidoterapia: str = ""
    pendencias: str = ""
    valor_acumulado: float = 0.0


class InternacaoCreate(InternacaoBase):
    pass


class Internacao(InternacaoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data_entrada: datetime
    ativa: bool


class EstoqueItemBase(BaseModel):
    nome: str
    categoria: str = "Medicamento"
    lote: str = ""
    validade: str = ""
    quantidade: int = Field(default=0, ge=0)
    minimo: int = Field(default=0, ge=0)


class EstoqueItemCreate(EstoqueItemBase):
    pass


class EstoqueItem(EstoqueItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class LancamentoFinanceiroBase(BaseModel):
    descricao: str
    tipo: Literal["Receita", "Despesa"] = "Receita"
    valor: float = Field(default=0.0, gt=0)
    status: Literal["Pago", "Pendente"] = "Pendente"


class LancamentoFinanceiroCreate(LancamentoFinanceiroBase):
    pass


class LancamentoFinanceiro(LancamentoFinanceiroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data: datetime


class FuncionarioBase(BaseModel):
    nome: str
    cargo: str = ""
    escala: str = ""
    comissao: str = ""


class FuncionarioCreate(FuncionarioBase):
    pass


class Funcionario(FuncionarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ItemVenda(BaseModel):
    nome: str
    preco: float = Field(gt=0)
    quantidade: int = Field(gt=0)


class VendaCreate(BaseModel):
    itens: list[ItemVenda] = Field(min_length=1)


class Venda(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data: datetime
    total: float
    itens_descricao: str
