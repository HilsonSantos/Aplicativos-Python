"""Popula o banco de dados com dados de exemplo, para facilitar testes manuais.

Executar com: poetry run python -m appvet.seed
"""

from datetime import datetime, timedelta

from appvet.database import SessionLocal, init_db
from appvet.models import (
    Agendamento,
    EstoqueItem,
    Funcionario,
    LancamentoFinanceiro,
    Paciente,
    Tutor,
)


def run() -> None:
    init_db()
    db = SessionLocal()

    if db.query(Tutor).first():
        print("Banco já contém dados. Nada a fazer.")
        return

    marina = Tutor(
        nome="Marina Alves",
        telefone="(81) 99123-4455",
        email="marina.alves@email.com",
        endereco="Rua das Graças, 120 - Recife/PE",
        documento="123.456.789-00",
    )
    carlos = Tutor(
        nome="Carlos Menezes",
        telefone="(81) 98877-2211",
        email="carlos.mnz@email.com",
        endereco="Av. Boa Viagem, 890 - Recife/PE",
        documento="987.654.321-00",
    )
    db.add_all([marina, carlos])
    db.flush()

    thor = Paciente(
        tutor_id=marina.id, nome="Thor", especie="Cão", raca="Golden Retriever",
        sexo="Macho", idade="4 anos", peso="32 kg", pelagem="Dourada",
        microchip="985141000345678", alergias="Nenhuma conhecida",
        doencas="Displasia leve de quadril", medicamentos="Nenhum em uso",
        vacinas="V10, Antirrábica (em dia)",
    )
    bidu = Paciente(
        tutor_id=carlos.id, nome="Bidu", especie="Cão", raca="Poodle",
        sexo="Macho", idade="7 anos", peso="6.2 kg", pelagem="Branca",
        microchip="985141000398365", alergias="Nenhuma conhecida",
        doencas="Doença renal crônica estágio 2", medicamentos="Benazepril 5mg 1x/dia",
        vacinas="V8 (atrasada)",
    )
    db.add_all([thor, bidu])
    db.flush()

    amanha = datetime.utcnow() + timedelta(days=1)
    db.add_all([
        Agendamento(
            paciente_id=thor.id, data_hora=amanha.replace(hour=8, minute=30),
            tipo="Consulta", veterinario="Dra. Fernanda", status="Confirmado",
        ),
        Agendamento(
            paciente_id=bidu.id, data_hora=amanha.replace(hour=10, minute=0),
            tipo="Retorno", veterinario="Dra. Fernanda", status="Confirmado",
        ),
    ])

    db.add_all([
        EstoqueItem(nome="Amoxicilina 250mg", categoria="Medicamento", lote="L2201",
                    validade="10/2026", quantidade=42, minimo=20),
        EstoqueItem(nome="Seringa 5ml", categoria="Material", lote="L1187",
                    validade="-", quantidade=8, minimo=30),
        EstoqueItem(nome="Ração Premium Cães 15kg", categoria="Pet shop", lote="-",
                    validade="03/2027", quantidade=15, minimo=5),
    ])

    db.add_all([
        LancamentoFinanceiro(descricao="Consulta - Thor", tipo="Receita", valor=180, status="Pago"),
        LancamentoFinanceiro(
            descricao="Fornecedor - VetMed Distribuidora", tipo="Despesa", valor=1240,
            status="Pendente",
        ),
    ])

    db.add_all([
        Funcionario(nome="Dra. Fernanda Lima", cargo="Veterinária",
                    escala="Seg-Sex, 08h-17h", comissao="20% consultas"),
        Funcionario(nome="Dr. Rodrigo Nunes", cargo="Veterinário",
                    escala="Ter-Sáb, 12h-21h", comissao="20% consultas"),
    ])

    db.commit()
    db.close()
    print("Banco populado com dados de exemplo.")


if __name__ == "__main__":
    run()
