# APPVET

Sistema de gestão para clínica veterinária — API em **FastAPI + SQLAlchemy** e
interface web em **Streamlit**.

> Este é o backend inicial do projeto (etapa 2, depois do protótipo de
> front-end em React). Cobre: tutores e pacientes, agenda, prontuário
> eletrônico, internação, documentos (modelos), estoque, financeiro, vendas/
> caixa e funcionários.

## Requisitos

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

## Instalação

```bash
poetry install
```

## Rodando a API

```bash
poetry run uvicorn appvet.main:app --reload
```

A API sobe em `http://localhost:8000`. Documentação interativa em
`http://localhost:8000/docs`.

Por padrão, os dados ficam em um arquivo SQLite (`appvet.db`) criado na raiz
do projeto. Para usar outro banco (Postgres, MySQL etc.), defina a variável
de ambiente `APPVET_DATABASE_URL`, por exemplo:

```bash
export APPVET_DATABASE_URL="postgresql://usuario:senha@localhost:5432/appvet"
```

### Popular com dados de exemplo (opcional)

```bash
poetry run python -m appvet.seed
```

## Rodando a interface (Streamlit)

Em outro terminal, com a API já rodando:

```bash
poetry run streamlit run streamlit_app/app.py
```

Por padrão o Streamlit conecta na API em `http://localhost:8000`. Para
apontar para outro endereço, defina `APPVET_API_URL`.

## Qualidade de código

```bash
poetry run ruff check .      # lint
poetry run ruff format .     # formatação
poetry run pytest            # testes automatizados
```

## Estrutura do projeto

```
appvet/
├── appvet/                  # backend (FastAPI + SQLAlchemy)
│   ├── main.py               # app FastAPI, monta as rotas
│   ├── database.py           # engine/sessão do banco
│   ├── models.py             # modelos ORM (SQLAlchemy)
│   ├── schemas.py            # schemas Pydantic (entrada/saída da API)
│   ├── seed.py                # popular banco com dados de exemplo
│   └── routers/               # um arquivo de rotas por módulo
├── streamlit_app/            # frontend (Streamlit)
│   ├── app.py                 # painel principal
│   ├── api_client.py          # cliente HTTP para a API
│   └── pages/                 # uma página por módulo
└── tests/                    # testes automatizados (pytest)
```

## Próximos passos sugeridos

1. Autenticação e perfis de acesso por função (recepção, veterinário, admin)
2. Geração real de PDF nos documentos e assinatura digital
3. Regras automáticas de comissão e repasse no financeiro
4. Migrations com Alembic em vez de `create_all`
5. Deploy (Docker Compose com API + banco + Streamlit)
