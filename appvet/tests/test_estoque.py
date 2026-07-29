"""Testes das rotas de estoque."""


def test_criar_item_estoque(client):
    resp = client.post(
        "/estoque/",
        json={"nome": "Amoxicilina 250mg", "categoria": "Medicamento", "quantidade": 40, "minimo": 20},
    )
    assert resp.status_code == 201
    assert resp.json()["quantidade"] == 40


def test_baixa_de_estoque(client):
    item = client.post("/estoque/", json={"nome": "Seringa 5ml", "quantidade": 10, "minimo": 5}).json()

    resp = client.patch(f"/estoque/{item['id']}/baixa", params={"quantidade": 3})
    assert resp.status_code == 200
    assert resp.json()["quantidade"] == 7


def test_baixa_insuficiente_retorna_erro(client):
    item = client.post("/estoque/", json={"nome": "Fluido Ringer", "quantidade": 2, "minimo": 5}).json()

    resp = client.patch(f"/estoque/{item['id']}/baixa", params={"quantidade": 10})
    assert resp.status_code == 400
