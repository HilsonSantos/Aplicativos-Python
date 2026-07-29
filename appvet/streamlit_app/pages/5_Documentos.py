"""Página de geração de documentos a partir de modelos."""

from datetime import date

import streamlit as st
from api_client import get

st.set_page_config(page_title="APPVET · Documentos", page_icon="🐾", layout="wide")
st.title("Documentos")

MODELOS = [
    "Termo de internação", "Termo de cirurgia", "Termo de anestesia", "Termo de alta",
    "Alta a pedido", "Autorização de eutanásia", "Recusa de tratamento", "Receituário",
]

pacientes = get("/tutores/pacientes/todos")
tutores = get("/tutores/")
tutor_por_paciente_id = {}
for t in tutores:
    for p in t["pacientes"]:
        tutor_por_paciente_id[p["id"]] = t["nome"]

col1, col2 = st.columns([1, 2])
with col1:
    modelo = st.radio("Modelo de documento", MODELOS)

with col2:
    if not pacientes:
        st.info("Cadastre um paciente para gerar documentos.")
        st.stop()
    mapa = {f"{p['nome']} — #{p['id']}": p for p in pacientes}
    nome_paciente = st.selectbox("Paciente", list(mapa.keys()))
    paciente = mapa[nome_paciente]
    tutor_nome = tutor_por_paciente_id.get(paciente["id"], "")

    st.markdown(f"### {modelo.upper()}")
    st.markdown(
        f"""
        Eu, **{tutor_nome}**, tutor(a) responsável pelo animal **{paciente['nome']}**,
        {paciente['especie'].lower()} da raça {paciente['raca']}, declaro estar ciente das
        informações e procedimentos referentes a este termo, prestados pela clínica
        veterinária, autorizando os procedimentos necessários conforme orientação do
        médico veterinário responsável.

        Recife, {date.today().strftime('%d de %B de %Y')}.

        &nbsp;

        _______________________________________
        Assinatura do tutor
        """
    )
    st.button("Gerar PDF", disabled=True, help="Geração de PDF será implementada na próxima etapa")
