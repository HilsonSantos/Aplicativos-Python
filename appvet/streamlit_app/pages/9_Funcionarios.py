"""Página de funcionários e prestadores."""

import streamlit as st
from api_client import get, post

st.set_page_config(page_title="APPVET · Funcionários", page_icon="🐾", layout="wide")
st.title("Funcionários")

with st.expander("➕ Cadastrar funcionário"):
    with st.form("form_funcionario", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome")
        cargo = col2.text_input("Cargo")
        col3, col4 = st.columns(2)
        escala = col3.text_input("Escala (ex: Seg-Sex, 08h-17h)")
        comissao = col4.text_input("Comissão (ex: 20% consultas)")
        if st.form_submit_button("Salvar") and nome:
            post("/funcionarios/", {"nome": nome, "cargo": cargo, "escala": escala, "comissao": comissao})
            st.success("Funcionário cadastrado.")
            st.rerun()

funcionarios = get("/funcionarios/")
if not funcionarios:
    st.info("Nenhum funcionário cadastrado.")
for f in funcionarios:
    with st.container(border=True):
        st.write(f"**{f['nome']}** — {f['cargo']}")
        st.caption(f"Escala: {f['escala']} · Comissão: {f['comissao']}")
