"""Página de cadastro de tutores e pacientes."""

import streamlit as st
from api_client import get, post

st.set_page_config(page_title="APPVET · Tutores", page_icon="🐾", layout="wide")
st.title("Tutores e pacientes")

with st.expander("➕ Cadastrar novo tutor"):
    with st.form("form_tutor", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome completo")
        telefone = col2.text_input("Telefone")
        email = col1.text_input("E-mail")
        documento = col2.text_input("Documento (CPF)")
        endereco = st.text_input("Endereço")
        if st.form_submit_button("Salvar tutor") and nome:
            post("/tutores/", {
                "nome": nome, "telefone": telefone, "email": email,
                "documento": documento, "endereco": endereco,
            })
            st.success("Tutor cadastrado.")
            st.rerun()

busca = st.text_input("🔍 Buscar por tutor ou paciente")
tutores = get("/tutores/")

if busca:
    tutores = [
        t for t in tutores
        if busca.lower() in t["nome"].lower()
        or any(busca.lower() in p["nome"].lower() for p in t["pacientes"])
    ]

for tutor in tutores:
    with st.container(border=True):
        st.markdown(f"### {tutor['nome']}")
        st.caption(f"{tutor['telefone']} · {tutor['email']} · {tutor['endereco']}")

        cols = st.columns(3)
        for idx, paciente in enumerate(tutor["pacientes"]):
            with cols[idx % 3]:
                st.info(
                    f"**{paciente['nome']}** ({paciente['especie']})\n\n"
                    f"{paciente['raca']} · {paciente['sexo']} · {paciente['idade']} · {paciente['peso']}\n\n"
                    f"Alergias: {paciente['alergias'] or 'nenhuma'}"
                )

        with st.expander(f"➕ Adicionar paciente para {tutor['nome']}"):
            with st.form(f"form_paciente_{tutor['id']}", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                p_nome = c1.text_input("Nome do animal", key=f"p_nome_{tutor['id']}")
                p_especie = c2.selectbox("Espécie", ["Cão", "Gato", "Outro"], key=f"p_esp_{tutor['id']}")
                p_raca = c3.text_input("Raça", key=f"p_raca_{tutor['id']}")
                c4, c5, c6 = st.columns(3)
                p_sexo = c4.selectbox("Sexo", ["Macho", "Fêmea"], key=f"p_sexo_{tutor['id']}")
                p_idade = c5.text_input("Idade", key=f"p_idade_{tutor['id']}")
                p_peso = c6.text_input("Peso", key=f"p_peso_{tutor['id']}")
                p_alergias = st.text_input("Alergias", key=f"p_alerg_{tutor['id']}")
                p_doencas = st.text_input("Doenças anteriores", key=f"p_doe_{tutor['id']}")
                p_vacinas = st.text_input("Vacinas", key=f"p_vac_{tutor['id']}")
                if st.form_submit_button("Salvar paciente") and p_nome:
                    post(f"/tutores/{tutor['id']}/pacientes", {
                        "nome": p_nome, "especie": p_especie, "raca": p_raca,
                        "sexo": p_sexo, "idade": p_idade, "peso": p_peso,
                        "alergias": p_alergias, "doencas": p_doencas, "vacinas": p_vacinas,
                    })
                    st.success("Paciente cadastrado.")
                    st.rerun()

if not tutores:
    st.info("Nenhum tutor encontrado.")
