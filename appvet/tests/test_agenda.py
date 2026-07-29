"""Testes das rotas de agenda."""


def _criar_paciente(client):
    tutor = client.post("/tutores/", json={"nome": "Ana Souza"}).json()
    paciente = client.post(
        f"/tutores/{tutor['id']}/pacientes", json={"nome": "Rex", "especie": "Cão"}
    ).json()
    return paciente


def test_criar_agendamento(client):
    paciente = _criar_paciente(client)
    resp = client.post(
        "/agenda/",
        json={
            "paciente_id": paciente["id"],
            "data_hora": "2026-07-21T09:00:00",
            "tipo": "Consulta",
            "veterinario": "Dra. Fernanda",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "Aguardando"


def test_atualizar_status_agendamento(client):
    paciente = _criar_paciente(client)
    agendamento = client.post(
        "/agenda/",
        json={"paciente_id": paciente["id"], "data_hora": "2026-07-21T09:00:00"},
    ).json()

    resp = client.patch(f"/agenda/{agendamento['id']}/status", json={"status": "Confirmado"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "Confirmado"


def test_atualizar_status_agendamento_inexistente(client):
    resp = client.patch("/agenda/999/status", json={"status": "Confirmado"})
    assert resp.status_code == 404
