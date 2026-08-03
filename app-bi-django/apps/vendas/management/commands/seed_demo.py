from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.vendas.models import Venda


class Command(BaseCommand):
    help = "Cria dados de demonstração para o BI."

    def handle(self, *args, **options):
        Venda.objects.all().delete()

        dados = [
            ("Ana", "Cliente A", "Produto 1", "Bebidas", 12000),
            ("Bruno", "Cliente B", "Produto 2", "Alimentos", 18500),
            ("Carla", "Cliente C", "Produto 3", "Higiene", 9200),
            ("Ana", "Cliente D", "Produto 4", "Bebidas", 22100),
            ("Bruno", "Cliente E", "Produto 5", "Alimentos", 15700),
            ("Carla", "Cliente F", "Produto 6", "Higiene", 11300),
        ]

        for index, item in enumerate(dados, start=1):
            vendedor, cliente, produto, categoria, valor = item
            Venda.objects.create(
                data=date(2026, index, 15),
                vendedor=vendedor,
                cliente=cliente,
                produto=produto,
                categoria=categoria,
                quantidade=index * 10,
                valor=Decimal(str(valor)),
                meta=Decimal("20000"),
            )

        self.stdout.write(self.style.SUCCESS("Dados de demonstração criados."))
