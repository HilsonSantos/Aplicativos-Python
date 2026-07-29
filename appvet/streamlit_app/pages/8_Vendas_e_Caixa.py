"""Página de vendas e frente de caixa."""

import streamlit as st
from api_client import post

st.set_page_config(page_title="APPVET · Vendas e caixa", page_icon="🐾", layout="wide")
st.title("Vendas e caixa")

PRODUTOS = [
    {"nome": "Consulta clínica", "preco": 180.0},
    {"nome": "Vacina V10", "preco": 95.0},
    {"nome": "Banho e tosa (porte médio)", "preco": 70.0},
    {"nome": "Ração Premium 15kg", "preco": 240.0},
    {"nome": "Exame de sangue completo", "preco": 150.0},
]

if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Produtos e serviços")
    prod_cols = st.columns(2)
    for idx, produto in enumerate(PRODUTOS):
        with prod_cols[idx % 2]:
            with st.container(border=True):
                st.write(f"**{produto['nome']}**")
                st.caption(f"R$ {produto['preco']:.2f}")
                if st.button("Adicionar", key=f"add_{produto['nome']}"):
                    st.session_state.carrinho[produto["nome"]] = (
                        st.session_state.carrinho.get(produto["nome"], 0) + 1
                    )
                    st.rerun()

with col2:
    st.subheader("🧾 Caixa")
    total = 0.0
    if not st.session_state.carrinho:
        st.info("Nenhum item no carrinho.")
    for nome, qtd in list(st.session_state.carrinho.items()):
        preco = next(p["preco"] for p in PRODUTOS if p["nome"] == nome)
        subtotal = preco * qtd
        total += subtotal
        c1, c2 = st.columns([3, 1])
        c1.write(f"{qtd}x {nome} — R$ {subtotal:.2f}")
        if c2.button("✕", key=f"rm_{nome}"):
            del st.session_state.carrinho[nome]
            st.rerun()

    st.markdown(f"### Total: R$ {total:.2f}")
    if st.button("Finalizar venda", type="primary", disabled=not st.session_state.carrinho):
        itens = [
            {"nome": nome, "preco": next(p["preco"] for p in PRODUTOS if p["nome"] == nome), "quantidade": qtd}
            for nome, qtd in st.session_state.carrinho.items()
        ]
        post("/vendas/", {"itens": itens})
        st.session_state.carrinho = {}
        st.success("Venda finalizada com sucesso.")
        st.rerun()
