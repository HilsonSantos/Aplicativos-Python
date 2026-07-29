# Controle de Equipamentos de TI

Ferramenta interna para cadastro, empréstimo e histórico de equipamentos de informática
(Celulares, CPUs e Notebooks).

## Stack

- **Python 3.11+**
- **Poetry** — gerenciamento de dependências
- **FastAPI** — API REST
- **SQLAlchemy** — ORM / banco de dados (SQLite por padrão)
- **Streamlit** — interface web
- **Ruff** — lint
- **Pytest** — testes

## Estrutura

```
equipamentos-ti/
├── app/
│   ├── database.py   # conexão e sessão do banco
│   ├── models.py      # modelos SQLAlchemy (Equipamento, Histórico)
│   ├── schemas.py      # schemas Pydantic
│   ├── crud.py         # regras de acesso a dados
│   └── main.py         # rotas da API FastAPI
├── frontend/
│   └── streamlit_app.py  # interface web
└── tests/
    └── test_api.py       # testes automatizados
```

## Como rodar

1. Instalar dependências:
   ```bash
   poetry install
   ```

2. Subir a API (porta 8000):
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
   Documentação interativa em `http://localhost:8000/docs`.

3. Em outro terminal, subir a interface:
   ```bash
   poetry run streamlit run frontend/streamlit_app.py
   ```

4. Rodar os testes:
   ```bash
   poetry run pytest
   ```

5. Rodar o lint:
   ```bash
   poetry run ruff check .
   ```

## Funcionalidades

- Cadastro de equipamentos por tipo (Celular, CPU, Notebook), com tag automática (ex: `NTB-A1B2C`)
- Controle de responsável atual, status (em uso / manutenção / estoque), data de aquisição e valor
- Movimentação/empréstimo com atualização automática do histórico
- Histórico completo por equipamento
- Filtros por tipo, status e busca por tag/modelo/responsável
- Painel com estatísticas (total, em uso, manutenção, estoque)

## Banco de dados

Por padrão usa SQLite (`equipamentos.db`, criado automaticamente na primeira execução).
Para usar outro banco (ex: PostgreSQL), defina a variável de ambiente `DATABASE_URL`:

```bash
export DATABASE_URL="postgresql://usuario:senha@localhost/equipamentos"
```
