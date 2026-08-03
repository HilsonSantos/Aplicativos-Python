google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(() => {
    carregarDashboard();
    }
);

async function carregarDashboard(refresh = false) {
    let url = "/api/vendas/dashboard/";

    if (refresh) {
        url += "?refresh=true";
    }
    const response = await fetch(url);
    const data = await response.json();

    document.getElementById("faturamento").textContent =
        data.kpis.faturamento.toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        });

    document.getElementById("pedidos").textContent = data.kpis.pedidos;
    document.getElementById("clientes").textContent = data.kpis.clientes;

    desenharMensal(data.mensal);
    desenharSegmentos(data.segmentos);
    desenharRepresentantes(data.representantes);
}

function desenharMensal(items) {
    const rows = [["Mês", "Faturamento"]];
    items.forEach(item => rows.push([item.mes, item.total]));

    const data = google.visualization.arrayToDataTable(rows);

    const chart = new google.visualization.LineChart(
        document.getElementById("chart_mensal")
    );

    chart.draw(data,
        {
            legend: { position: "none" },
            curveType: "function",
            height: 350,
            chartArea: { width: "85%", height: "70%" },
        }
    );
}

function desenharSegmentos(items) {
    const rows = [["Segmento", "Vendas"]];
    items.forEach(item => rows.push([item.segmento, item.total]));

    const data = google.visualization.arrayToDataTable(rows);

    const chart = new google.visualization.PieChart(
        document.getElementById("chart_vendedores")
    );

    chart.draw(data,
        {
            legend: { position: "right" },
            height: 350,
            chartArea: { width: "80%", height: "70%" },
            pieHole: 0.4,
        }
    );
}

function desenharRepresentantes(items) {
    const rows = [["Representantes", "Vendas"]];
    items.forEach(item => rows.push([item.representante, item.total]));

    const data = google.visualization.arrayToDataTable(rows);

    const chart = new google.visualization.BarChart(
        document.getElementById("chart_categorias")
    );

    chart.draw(data,
        {
            legend: { position: "none" },
            pieHole: 0.4,
            height: 350,
            chartArea: { width: "50%", height: "80%" },
        }
    );
}
