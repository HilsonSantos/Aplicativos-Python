"""Página do módulo financeiro."""

import streamlit as st
from api_client import get, patch, post

st.set_page_config(page_title="APPVET · Financeiro", page_icon="🐾", layout="wide")
st.title("Financeiro")

resumo = get("/financeiro/resumo/totais")
col1, col2, col3 = st.columns(3)
col1.metric("Receitas", f"R$ {resumo['receitas']:.2f}")
col2.metric("Despesas", f"R$ {resumo['despesas']:.2f}")
col3.metric("Saldo", f"R$ {resumo['saldo']:.2f}")

with st.expander("➕ Novo lançamento"):
    with st.form("form_financeiro", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        descricao = col1.text_input("Descrição")
        tipo = col2.selectbox("Tipo", ["Receita", "Despesa"])
        valor = col3.number_input("Valor (R$)", min_value=0.0, step=10.0)
        if st.form_submit_button("Salvar lançamento") and descricao:
            post("/financeiro/", {"descricao": descricao, "tipo": tipo, "valor": valor, "status": "Pendente"})
            st.success("Lançamento registrado.")
            st.rerun()

lancamentos = get("/financeiro/")
for lanc in lancamentos:
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
        c1.write(f"**{lanc['descricao']}**")
        c2.caption(lanc["data"][:10])
        cor = "green" if lanc["tipo"] == "Receita" else "red"
        c3.markdown(f":{cor}[{lanc['tipo']} — R$ {lanc['valor']:.2f}]")
        novo_status = c4.selectbox(
            "Status", ["Pendente", "Pago"], index=["Pendente", "Pago"].index(lanc["status"]),
            key=f"fin_status_{lanc['id']}", label_visibility="collapsed",
        )
        if novo_status != lanc["status"]:
            patch(f"/financeiro/{lanc['id']}/status", params={"status": novo_status})
            st.rerun()

if not lancamentos:
    st.info("Nenhum lançamento registrado.")
