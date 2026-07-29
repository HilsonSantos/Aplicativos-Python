"""Testes das rotas de financeiro e vendas."""


def test_resumo_financeiro(client):
    client.post("/financeiro/", json={"descricao": "Consulta", "tipo": "Receita", "valor": 180, "status": "Pago"})
    client.post("/financeiro/", json={"descricao": "Fornecedor", "tipo": "Despesa", "valor": 100, "status": "Pago"})

    resp = client.get("/financeiro/resumo/totais")
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["receitas"] == 180
    assert dados["despesas"] == 100
    assert dados["saldo"] == 80


def test_finalizar_venda_gera_lancamento_financeiro(client):
    resp = client.post(
        "/vendas/",
        json={"itens": [{"nome": "Vacina V10", "preco": 95.0, "quantidade": 2}]},
    )
    assert resp.status_code == 201
    assert resp.json()["total"] == 190.0

    lancamentos = client.get("/financeiro/").json()
    assert any(l["valor"] == 190.0 for l in lancamentos)
