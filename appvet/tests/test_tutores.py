"""Testes das rotas de tutores e pacientes."""


def test_criar_e_listar_tutor(client):
    resp = client.post("/tutores/", json={"nome": "Marina Alves", "telefone": "81999999999"})
    assert resp.status_code == 201
    tutor = resp.json()
    assert tutor["nome"] == "Marina Alves"
    assert tutor["pacientes"] == []

    resp = client.get("/tutores/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_criar_paciente_vinculado_a_tutor(client):
    tutor = client.post("/tutores/", json={"nome": "Carlos Menezes"}).json()

    resp = client.post(
        f"/tutores/{tutor['id']}/pacientes",
        json={"nome": "Thor", "especie": "Cão", "raca": "Golden Retriever"},
    )
    assert resp.status_code == 201
    paciente = resp.json()
    assert paciente["tutor_id"] == tutor["id"]

    resp = client.get(f"/tutores/{tutor['id']}")
    assert len(resp.json()["pacientes"]) == 1


def test_criar_paciente_para_tutor_inexistente_retorna_404(client):
    resp = client.post("/tutores/999/pacientes", json={"nome": "Fantasma"})
    assert resp.status_code == 404


def test_excluir_tutor(client):
    tutor = client.post("/tutores/", json={"nome": "Tutor Temporário"}).json()
    resp = client.delete(f"/tutores/{tutor['id']}")
    assert resp.status_code == 204
    assert client.get(f"/tutores/{tutor['id']}").status_code == 404
