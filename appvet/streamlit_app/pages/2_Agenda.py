"""Página de agenda e agendamentos."""

from datetime import date, datetime, time

import streamlit as st
from api_client import get, patch, post

st.set_page_config(page_title="APPVET · Agenda", page_icon="🐾", layout="wide")
st.title("Agenda")

pacientes = get("/tutores/pacientes/todos")
mapa_pacientes = {f"{p['nome']} — #{p['id']}": p["id"] for p in pacientes}

with st.expander("➕ Novo agendamento"):
    with st.form("form_agendamento", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        paciente_nome = col1.selectbox("Paciente", list(mapa_pacientes.keys()) or ["Cadastre um paciente antes"])
        data_agendamento = col2.date_input("Data", value=date.today())
        hora_agendamento = col3.time_input("Horário", value=time(9, 0))
        col4, col5 = st.columns(2)
        tipo = col4.selectbox("Tipo", ["Consulta", "Retorno", "Vacina", "Exame", "Cirurgia", "Banho e tosa"])
        veterinario = col5.text_input("Veterinário responsável")
        if st.form_submit_button("Agendar") and paciente_nome in mapa_pacientes:
            data_hora = datetime.combine(data_agendamento, hora_agendamento)
            post("/agenda/", {
                "paciente_id": mapa_pacientes[paciente_nome],
                "data_hora": data_hora.isoformat(),
                "tipo": tipo,
                "veterinario": veterinario,
                "status": "Aguardando",
            })
            st.success("Agendamento criado.")
            st.rerun()

agendamentos = get("/agenda/")
id_para_nome = {p["id"]: p["nome"] for p in pacientes}

status_opcoes = ["Aguardando", "Confirmado", "Encaixe", "Atendido", "Falta"]

for a in agendamentos:
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(
            f"**{a['data_hora'][:16].replace('T', ' ')}** — "
            f"{id_para_nome.get(a['paciente_id'], '?')} ({a['tipo']})"
        )
        col2.caption(a["veterinario"])
        novo_status = col3.selectbox(
            "Status", status_opcoes, index=status_opcoes.index(a["status"]),
            key=f"status_{a['id']}", label_visibility="collapsed",
        )
        if novo_status != a["status"]:
            patch(f"/agenda/{a['id']}/status", {"status": novo_status})
            st.rerun()

if not agendamentos:
    st.info("Nenhum agendamento cadastrado.")
