import pytest
from django.urls import reverse

from apps.vendas.models import Venda


@pytest.mark.django_db
def test_dashboard_data(client):
    Venda.objects.create(
        data="2026-01-01",
        vendedor="Ana",
        cliente="Cliente A",
        produto="Produto A",
        categoria="Bebidas",
        quantidade=1,
        valor=1000,
        meta=1200,
    )

    response = client.get(reverse("dashboard-data"))

    assert response.status_code == 200
    assert response.json()["kpis"]["faturamento"] == 1000.0
    assert response.json()["kpis"]["clientes"] == 1
