"""Página de prontuário eletrônico."""

import streamlit as st
from api_client import get, post

st.set_page_config(page_title="APPVET · Prontuário", page_icon="🐾", layout="wide")
st.title("Prontuário eletrônico")

pacientes = get("/tutores/pacientes/todos")
if not pacientes:
    st.info("Cadastre um paciente antes de usar o prontuário.")
    st.stop()

mapa_pacientes = {f"{p['nome']} — #{p['id']}": p for p in pacientes}
nome_selecionado = st.selectbox("Paciente", list(mapa_pacientes.keys()))
paciente = mapa_pacientes[nome_selecionado]

with st.container(border=True):
    st.markdown(f"#### Ficha clínica — {paciente['nome']}")
    c1, c2, c3 = st.columns(3)
    c1.write(f"**Espécie/raça:** {paciente['especie']} · {paciente['raca']}")
    c2.write(f"**Idade/peso:** {paciente['idade']} · {paciente['peso']}")
    c3.write(f"**Microchip:** {paciente['microchip']}")
    c4, c5 = st.columns(2)
    c4.write(f"**Alergias:** {paciente['alergias']}")
    c5.write(f"**Vacinas:** {paciente['vacinas']}")

with st.expander("➕ Registrar novo atendimento"):
    with st.form("form_prontuario", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        vet = col1.text_input("Veterinário")
        peso = col2.text_input("Peso")
        temperatura = col3.text_input("Temperatura")
        queixa = st.text_input("Queixa principal")
        exame = st.text_area("Exame físico", height=80)
        diagnostico = st.text_input("Diagnóstico")
        prescricao = st.text_area("Prescrição", height=80)
        if st.form_submit_button("Salvar evolução") and queixa:
            post("/prontuario/", {
                "paciente_id": paciente["id"], "veterinario": vet, "peso": peso,
                "temperatura": temperatura, "queixa": queixa, "exame": exame,
                "diagnostico": diagnostico, "prescricao": prescricao,
            })
            st.success("Evolução registrada.")
            st.rerun()

st.subheader("Histórico de evoluções")
entradas = get(f"/prontuario/{paciente['id']}")
if not entradas:
    st.info("Nenhuma evolução registrada para este paciente.")
for e in entradas:
    with st.container(border=True):
        st.write(f"**{e['data'][:16].replace('T', ' ')}** — {e['veterinario']}")
        st.write(f"Queixa: {e['queixa']}")
        st.write(f"Exame físico: {e['exame']}")
        st.write(f"Diagnóstico: {e['diagnostico']}")
        st.write(f"Prescrição: {e['prescricao']}")
