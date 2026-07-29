"""Modelos ORM (SQLAlchemy) do APPVET."""

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from appvet.database import Base


class Tutor(Base):
    __tablename__ = "tutores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150))
    telefone: Mapped[str] = mapped_column(String(30), default="")
    email: Mapped[str] = mapped_column(String(150), default="")
    endereco: Mapped[str] = mapped_column(String(255), default="")
    documento: Mapped[str] = mapped_column(String(30), default="")

    pacientes: Mapped[list["Paciente"]] = relationship(
        back_populates="tutor", cascade="all, delete-orphan"
    )


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutores.id"))
    nome: Mapped[str] = mapped_column(String(150))
    especie: Mapped[str] = mapped_column(String(50), default="")
    raca: Mapped[str] = mapped_column(String(100), default="")
    sexo: Mapped[str] = mapped_column(String(20), default="")
    idade: Mapped[str] = mapped_column(String(30), default="")
    peso: Mapped[str] = mapped_column(String(30), default="")
    pelagem: Mapped[str] = mapped_column(String(100), default="")
    microchip: Mapped[str] = mapped_column(String(50), default="")
    alergias: Mapped[str] = mapped_column(String(255), default="")
    doencas: Mapped[str] = mapped_column(String(255), default="")
    medicamentos: Mapped[str] = mapped_column(String(255), default="")
    vacinas: Mapped[str] = mapped_column(String(255), default="")

    tutor: Mapped["Tutor"] = relationship(back_populates="pacientes")
    prontuarios: Mapped[list["ProntuarioEntrada"]] = relationship(
        back_populates="paciente", cascade="all, delete-orphan"
    )


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    data_hora: Mapped[datetime] = mapped_column(DateTime)
    tipo: Mapped[str] = mapped_column(String(50), default="Consulta")
    veterinario: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(30), default="Aguardando")

    paciente: Mapped["Paciente"] = relationship()


class ProntuarioEntrada(Base):
    __tablename__ = "prontuario_entradas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    veterinario: Mapped[str] = mapped_column(String(100), default="")
    queixa: Mapped[str] = mapped_column(String(255), default="")
    exame: Mapped[str] = mapped_column(String(500), default="")
    diagnostico: Mapped[str] = mapped_column(String(255), default="")
    prescricao: Mapped[str] = mapped_column(String(500), default="")
    peso: Mapped[str] = mapped_column(String(30), default="")
    temperatura: Mapped[str] = mapped_column(String(30), default="")

    paciente: Mapped["Paciente"] = relationship(back_populates="prontuarios")


class Internacao(Base):
    __tablename__ = "internacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    leito: Mapped[str] = mapped_column(String(50), default="")
    veterinario: Mapped[str] = mapped_column(String(100), default="")
    diagnostico: Mapped[str] = mapped_column(String(255), default="")
    data_entrada: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    previsao_alta: Mapped[str] = mapped_column(String(50), default="")
    fluidoterapia: Mapped[str] = mapped_column(String(255), default="")
    pendencias: Mapped[str] = mapped_column(String(500), default="")
    valor_acumulado: Mapped[float] = mapped_column(Float, default=0.0)
    ativa: Mapped[bool] = mapped_column(default=True)

    paciente: Mapped["Paciente"] = relationship()


class EstoqueItem(Base):
    __tablename__ = "estoque_itens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150))
    categoria: Mapped[str] = mapped_column(String(50), default="Medicamento")
    lote: Mapped[str] = mapped_column(String(50), default="")
    validade: Mapped[str] = mapped_column(String(20), default="")
    quantidade: Mapped[int] = mapped_column(Integer, default=0)
    minimo: Mapped[int] = mapped_column(Integer, default=0)


class LancamentoFinanceiro(Base):
    __tablename__ = "financeiro_lancamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    descricao: Mapped[str] = mapped_column(String(255))
    tipo: Mapped[str] = mapped_column(String(20), default="Receita")  # Receita | Despesa
    valor: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(20), default="Pendente")  # Pago | Pendente


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(150))
    cargo: Mapped[str] = mapped_column(String(100), default="")
    escala: Mapped[str] = mapped_column(String(150), default="")
    comissao: Mapped[str] = mapped_column(String(100), default="")


class Venda(Base):
    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total: Mapped[float] = mapped_column(Float, default=0.0)
    itens_descricao: Mapped[str] = mapped_column(String(500), default="")
