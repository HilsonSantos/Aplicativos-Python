"""Página de internação veterinária."""

import streamlit as st
from api_client import get, post

st.set_page_config(page_title="APPVET · Internação", page_icon="🐾", layout="wide")
st.title("Internação")

pacientes = get("/tutores/pacientes/todos")
mapa_pacientes = {f"{p['nome']} — #{p['id']}": p["id"] for p in pacientes}

with st.expander("➕ Internar paciente"):
    with st.form("form_internacao", clear_on_submit=True):
        col1, col2 = st.columns(2)
        paciente_nome = col1.selectbox("Paciente", list(mapa_pacientes.keys()) or ["Cadastre um paciente antes"])
        leito = col2.text_input("Leito / baia")
        col3, col4 = st.columns(2)
        veterinario = col3.text_input("Veterinário responsável")
        previsao_alta = col4.text_input("Previsão de alta (ex: 24/07/2026)")
        diagnostico = st.text_input("Diagnóstico")
        fluidoterapia = st.text_input("Fluidoterapia")
        pendencias = st.text_area("Pendências", height=70)
        if st.form_submit_button("Registrar internação") and paciente_nome in mapa_pacientes:
            post("/internacao/", {
                "paciente_id": mapa_pacientes[paciente_nome], "leito": leito,
                "veterinario": veterinario, "diagnostico": diagnostico,
                "previsao_alta": previsao_alta, "fluidoterapia": fluidoterapia,
                "pendencias": pendencias,
            })
            st.success("Internação registrada.")
            st.rerun()

internacoes = get("/internacao/")
id_para_nome = {p["id"]: p["nome"] for p in pacientes}

cols = st.columns(2)
for idx, i in enumerate(internacoes):
    with cols[idx % 2]:
        with st.container(border=True):
            st.markdown(f"#### 🛏️ {id_para_nome.get(i['paciente_id'], '?')} — Leito {i['leito']}")
            st.caption(f"Responsável: {i['veterinario']}")
            st.write(f"**Diagnóstico:** {i['diagnostico']}")
            st.write(f"**Fluidoterapia:** {i['fluidoterapia']}")
            st.write(f"**Entrada:** {i['data_entrada'][:16].replace('T', ' ')} · **Previsão de alta:** {i['previsao_alta']}")
            st.write(f"**Pendências:** {i['pendencias']}")
            st.write(f"**Valor acumulado:** R$ {i['valor_acumulado']:.2f}")
            if st.button("Registrar alta", key=f"alta_{i['id']}"):
                post(f"/internacao/{i['id']}/alta", {})
                st.rerun()

if not internacoes:
    st.info("Nenhum paciente internado no momento.")
