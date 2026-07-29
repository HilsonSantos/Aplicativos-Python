from app.termos import gerar_termo_pdf

EQUIPAMENTO = {
    "tag": "NTB-ABCDE",
    "tipo": "Notebook",
    "modelo": "Dell Latitude 5420",
    "responsavel": "Maria Souza",
    "status": "em_uso",
}


def test_gera_termo_de_responsabilidade_em_pdf():
    pdf = gerar_termo_pdf(EQUIPAMENTO, "responsabilidade")

    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 1_000


def test_gera_termo_de_devolucao_sem_responsavel():
    pdf = gerar_termo_pdf({**EQUIPAMENTO, "responsavel": None}, "devolucao")

    assert pdf.startswith(b"%PDF")
