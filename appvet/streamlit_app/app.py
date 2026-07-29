"""APPVET — Painel principal (Streamlit)."""

import streamlit as st
from api_client import get

st.set_page_config(page_title="APPVET · Painel", page_icon="🐾", layout="wide")

st.title("🐾 APPVET")
st.caption("Sistema de gestão para clínica veterinária")

try:
    tutores = get("/tutores/")
    agendamentos = get("/agenda/")
    internacoes = get("/internacao/")
    estoque = get("/estoque/")
    resumo = get("/financeiro/resumo/totais")
except Exception as exc:  # noqa: BLE001
    st.error(
        "Não foi possível conectar à API. Verifique se ela está em execução "
        f"(`poetry run uvicorn appvet.main:app --reload`).\n\nDetalhe: {exc}"
    )
    st.stop()

total_pacientes = sum(len(t["pacientes"]) for t in tutores)
baixo_estoque = [i for i in estoque if i["quantidade"] <= i["minimo"]]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Agendamentos", len(agendamentos))
col2.metric("Pacientes cadastrados", total_pacientes)
col3.metric("Internados", len(internacoes))
col4.metric("Saldo financeiro", f"R$ {resumo['saldo']:.2f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Próximos agendamentos")
    if not agendamentos:
        st.info("Nenhum agendamento cadastrado.")
    for a in agendamentos[:8]:
        st.write(f"**{a['data_hora'][:16].replace('T', ' ')}** — {a['tipo']} · {a['veterinario']} · `{a['status']}`")

with right:
    st.subheader("Alertas de estoque")
    if not baixo_estoque:
        st.success("Nenhum item abaixo do mínimo.")
    for item in baixo_estoque:
        st.warning(f"{item['nome']}: {item['quantidade']} em estoque (mínimo {item['minimo']})")

st.divider()
st.subheader("Pacientes internados")
if not internacoes:
    st.info("Nenhum paciente internado no momento.")
for i in internacoes:
    with st.container(border=True):
        st.write(f"**Leito {i['leito']}** — {i['diagnostico']}")
        st.caption(f"Previsão de alta: {i['previsao_alta']}")

st.sidebar.info("Use o menu acima para navegar entre os módulos: Tutores, Agenda, Prontuário, Internação, Documentos, Estoque, Financeiro, Vendas e Funcionários.")
