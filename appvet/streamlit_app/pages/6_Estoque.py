"""Página de estoque e medicamentos."""

import pandas as pd
import streamlit as st
from api_client import delete, get, post

st.set_page_config(page_title="APPVET · Estoque", page_icon="🐾", layout="wide")
st.title("Estoque")

with st.expander("➕ Cadastrar item"):
    with st.form("form_estoque", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        nome = col1.text_input("Nome")
        categoria = col2.selectbox("Categoria", ["Medicamento", "Material", "Material hospitalar", "Pet shop"])
        lote = col3.text_input("Lote")
        col4, col5, col6 = st.columns(3)
        validade = col4.text_input("Validade (mm/aaaa)")
        quantidade = col5.number_input("Quantidade", min_value=0, step=1)
        minimo = col6.number_input("Estoque mínimo", min_value=0, step=1)
        if st.form_submit_button("Salvar item") and nome:
            post("/estoque/", {
                "nome": nome, "categoria": categoria, "lote": lote,
                "validade": validade, "quantidade": int(quantidade), "minimo": int(minimo),
            })
            st.success("Item cadastrado.")
            st.rerun()

itens = get("/estoque/")
if not itens:
    st.info("Nenhum item cadastrado.")
    st.stop()

df = pd.DataFrame(itens)
df["alerta"] = df["quantidade"] <= df["minimo"]

for _, row in df.iterrows():
    with st.container(border=True):
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 1, 1])
        c1.write(f"**{row['nome']}**")
        c2.caption(f"{row['categoria']} · lote {row['lote']}")
        c3.caption(f"Validade: {row['validade']}")
        if row["alerta"]:
            c4.error(f"{row['quantidade']}")
        else:
            c4.write(f"{row['quantidade']}")
        if c5.button("Excluir", key=f"del_{row['id']}"):
            delete(f"/estoque/{row['id']}")
            st.rerun()
