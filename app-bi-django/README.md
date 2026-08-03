# APP BI Django

Aplicativo de Business Intelligence desenvolvido com Python, Django,
PostgreSQL e Google Charts.

## Tecnologias

- Python 3.13+
- Django
- Django REST Framework
- PostgreSQL
- Poetry
- Ruff
- Pytest
- Google Charts

## Instalação

```bash
poetry install
```

Copie o arquivo de ambiente:

```bash
copy .env.example .env
```

No Linux/macOS:

```bash
cp .env.example .env
```

Configure o PostgreSQL no arquivo `.env`.

Execute as migrations:

```bash
poetry run python manage.py migrate
```

Crie um usuário administrador:

```bash
poetry run python manage.py createsuperuser
```

Crie os dados de demonstração:

```bash
poetry run python manage.py seed_demo
```

Execute o servidor:

```bash
poetry run python manage.py runserver
```

Acesse:

http://127.0.0.1:8000/

Admin:

http://127.0.0.1:8000/admin/

API:

http://127.0.0.1:8000/api/vendas/dashboard/

## Qualidade

Executar Ruff:

```bash
poetry run ruff check .
```

Formatar:

```bash
poetry run ruff format .
```

Executar testes:

```bash
poetry run pytest
```

## Próximas evoluções

- Filtros por período
- Filtros por vendedor
- Metas e atingimento
- Ticket médio
- Margem de contribuição
- Top 10 clientes
- Top 10 produtos
- Exportação Excel
- Integração Oracle
- Integração SQL Server
- Integração PostgreSQL
- Controle de permissões por usuário
- Docker
- CI/CD
