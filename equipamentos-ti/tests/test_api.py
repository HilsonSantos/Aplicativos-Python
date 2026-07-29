def _criar_equipamento(client, **overrides):
    payload = {
        "tipo": "Notebook",
        "modelo": "Dell Latitude 5420",
        "responsavel": "Maria Souza",
        "status": "em_uso",
        "data_aquisicao": "2024-03-10",
        "valor": 4200.50,
        "observacao": "Uso do time financeiro",
    }
    payload.update(overrides)
    resp = client.post("/equipamentos", json=payload)
    assert resp.status_code == 201
    return resp.json()


def test_criar_equipamento_gera_tag_e_historico(client):
    equipamento = _criar_equipamento(client)
    assert equipamento["tag"].startswith("NTB-")

    detalhe = client.get(f"/equipamentos/{equipamento['id']}").json()
    assert len(detalhe["historico"]) == 1
    assert detalhe["historico"][0]["acao"] == "Cadastro"


def test_listar_com_filtros(client):
    _criar_equipamento(client, tipo="Celular", modelo="iPhone 13")
    _criar_equipamento(
        client,
        tipo="CPU",
        modelo="Optiplex 3080",
        status="estoque",
        responsavel=None,
    )

    apenas_celulares = client.get("/equipamentos", params={"tipo": "Celular"}).json()
    assert len(apenas_celulares) == 1
    assert apenas_celulares[0]["modelo"] == "iPhone 13"

    apenas_estoque = client.get("/equipamentos", params={"status": "estoque"}).json()
    assert len(apenas_estoque) == 1

    busca = client.get("/equipamentos", params={"q": "optiplex"}).json()
    assert len(busca) == 1

    busca_com_espacos = client.get("/equipamentos", params={"q": "  OPTIPLEX  "}).json()
    assert len(busca_com_espacos) == 1


def test_movimentar_equipamento_atualiza_status_e_historico(client):
    equipamento = _criar_equipamento(client, responsavel="João Lima", status="em_uso")

    resp = client.post(
        f"/equipamentos/{equipamento['id']}/movimentar",
        json={"responsavel": None, "status": "manutencao", "nota": "Tela quebrada"},
    )
    assert resp.status_code == 200
    atualizado = resp.json()
    assert atualizado["status"] == "manutencao"
    assert atualizado["responsavel"] is None

    detalhe = client.get(f"/equipamentos/{equipamento['id']}").json()
    assert len(detalhe["historico"]) == 2
    assert "Tela quebrada" in detalhe["historico"][-1]["detalhe"]


def test_estatisticas(client):
    _criar_equipamento(client, status="em_uso")
    _criar_equipamento(client, status="manutencao", tipo="CPU", modelo="Optiplex")
    _criar_equipamento(
        client,
        status="estoque",
        tipo="Celular",
        modelo="iPhone 13",
        responsavel=None,
    )

    stats = client.get("/equipamentos/estatisticas").json()
    assert stats == {"total": 3, "em_uso": 1, "manutencao": 1, "estoque": 1}


def test_excluir_equipamento(client):
    equipamento = _criar_equipamento(client)
    resp = client.delete(f"/equipamentos/{equipamento['id']}")
    assert resp.status_code == 204
    assert client.get(f"/equipamentos/{equipamento['id']}").status_code == 404


def test_equipamento_inexistente_retorna_404(client):
    assert client.get("/equipamentos/9999").status_code == 404
