from django.core.cache import cache
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse

from .models import FatVenda


def dashboard_data(request):
    ano = 2026
    mes = request.GET.get("mes")
    vendedor = request.GET.get("vendedor")

    cache_key = (
        f"dashboard_data:"
        f"ano={ano}:"
        f"mes={mes or 'todos'}:"
        f"vendedor={vendedor or 'todos'}"
    )

    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return JsonResponse(cached_data)

    vendas = FatVenda.objects.filter(data__year=ano)

    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez",
    }

    if mes:
        vendas = vendas.filter(data__month=mes)

    if vendedor:
        vendas = vendas.filter(vendedor=vendedor)

    total = vendas.aggregate(total=Sum("vendas_liquida"))["total"] or 0

    mensal = list(
        vendas.annotate(periodo=TruncMonth("data"))
        .values("periodo")
        .annotate(total=Sum("vendas_liquida"))
        .order_by("periodo")
    )

    segmentos = list(
        vendas.values(
            "segmento_id",
            "segmento__segmento_descricao"
        )
        .annotate(total=Sum("vendas_liquida"))
        .order_by("-total")[:5]
    )

    representantes = list(
        vendas.values(
            "representante_id",
            "representante__representante_nome"
        )
        .annotate(total=Sum("vendas_liquida"))
        .order_by("-total")[:10]
    )

    data = {
        "kpis": {
            "faturamento": float(total),
            "pedidos": vendas.count(),
            "clientes": vendas.values("cliente_id").distinct().count(),
        },
        "mensal": [
            {
                # "mes": item["periodo"].strftime("%B"),
                "mes": meses[item["periodo"].month],
                "total": float(item["total"])
            }
            for item in mensal
        ],
        "segmentos": [
            {
                "segmento": item["segmento__segmento_descricao"],
                "total": float(item["total"])
            }
            for item in segmentos
        ],
        "representantes": [
            {
                "representante": item["representante__representante_nome"],
                "total": float(item["total"])
            }
            for item in representantes
        ],
    }

    cache.set(
        cache_key,
        data,
        timeout=60 * 15,
    )

    return JsonResponse(data)
