"""Interface web (Streamlit) para o controle de equipamentos de TI."""

import os

import requests
import streamlit as st

from app.termos import gerar_termo_pdf

API_URL = os.getenv("API_URL", "http://localhost:8000")

TIPOS_LABELS = {
    "celular": "Celular",
    "computador": "Computador",
    "notebook": "Notebook",
    "impressora": "Impressora",
    "roteador": "Roteador",
}
TIPOS_KEYS = list(TIPOS_LABELS.keys())

STATUS_LABELS = {
    "em_uso": "Em uso",
    "manutencao": "Manutenção",
    "estoque": "Estoque",
    "descarte": "Descarte",
}
STATUS_KEYS = list(STATUS_LABELS.keys())

MARCAS_CEL = [
    "",
    "Apple",
    "Samsung",
    "Motorola",
    "Xiaomi",
    "Redmi",
    "POCO",
    "Huawei",
    "Google",
    "Nokia",
    "LG",
    "ASUS",
    "Sony",
    "OnePlus",
    "OPPO",
    "Realme",
    "Vivo",
    "Honor",
    "TCL",
    "ZTE",
    "Alcatel",
    "Multilaser",
    "Positivo",
    "Infinix",
    "Tecno",
]

MARCAS_CPU = [
    "",
    "Acer",
    "Apple",
    "ASUS",
    "Avell",
    "Braview",
    "CCE",
    "Compaq",
    "Dell",
    "HP",
    "Intel",
    "Lenovo",
    "LG",
    "Megaware",
    "Microsoft",
    "MSI",
    "Positivo",
    "Razer",
    "Samsung",
    "Vaio",
    "Xiaomi",
]

MARCAS_NTB = [
    "",
    "Acer",
    "Apple",
    "ASUS",
    "Dell",
    "HP",
    "Lenovo",
    "Samsung",
    "Microsoft",
    "MSI",
    "Razer",
]

MARCAS_IMP = [
    "",
    "Brother",
    "Canon",
    "Epson",
    "HP",
    "Lexmark",
    "Samsung",
    "Xerox",
    "Ricoh",
    "Kyocera",
    "Konica Minolta",
    "OKI",
    "Zebra",
    "Pantum",
    "Elgin",
    "Bematech",
    "Daruma",
    "Tanca",
    "Argox",
    "Honeywell",
    "Datamax",
]

MARCAS_ROT = [
    "",
    "TP-Link",
    "Intelbras",
    "Huawei",
    "ZTE",
    "Cisco",
    "D-Link",
    "MikroTik",
    "Ubiquiti",
    "HPE Aruba",
    "Fortinet",
    "Netgear",
    "Linksys",
    "ASUS",
    "Tenda",
    "Mercusys",
    "Multilaser",
    "Nokia",
    "Technicolor",
    "Zyxel",
    "Dell",
]

OPERADORAS = [
    "",
    "Claro",
    "Tim",
    "Vivo",
]

DEPARTAMENTOS = {
    "": {"": [],},
    "Diretoria": {
        "": [],
        "Diretoria": [
            "",
            "Diretor Executivo",
            "Gerente Geral",
        ],
    },
    "Comercial": {
        "": [],
        "Vendas": [
            "",
            "Diretor",
            "Gerente",
            "Supervisor",
            "Vendedor",
            "Representante",
        ],
        "Atendimento / SAC": [
            "",
            "Coordenador",
            "Analista",
        ],
    },
    "Compras": {
        "": [],
        "Compras": [
            "",
            "Gerente",
            "Coordenador",
            "Comprador",
        ],
        "Gestão de Fornecedores": [
            "",
            "Analista de Suprimentos",
        ],
    },
    "Financeiro": {
        "": [],
        "Financeiro": [
            "",
            "Gerente",
            "Contas a Pagar",
            "Contas a Receber",
            "Crédito",
            "Cobrança",
            "Tesouraria",
        ]
    },
    "Logística": {
        "": [],
        "Transportes": [
            "",
            "Gerente",
            "Coordenador",
            "Analista",
            "Motorista",
        ],
        "Armazenagem": [
            "",
            "Coordenador",
            "Supervisor",
            "Conferente",
            "Estoquista",
        ],
    },
    "Informática" : {
        "": [],
        "TI" : [
            "Gerente",
            "Suporte",
            "Desenvolvedor",
        ],
    },
    "Contabilidade" : {
        "": [],
        "Contábil / Fiscal" : [
            "Gerente",
            "Analista Contábil",
            "Analista Fiscal",
        ],
    },
    "Marketing" : {
        "": [],
        "Marketing" : [
            "Gerente",
            "Coordenador",
            "Analista",
            "Assistente",
        ],
    },
    "RH / Gestão Pessoal" : {
        "": [],
        "Recursos Humanos" : [
            "Gerente",
            "Coordenador",
            "Analista",
            "Assistente",
        ],
        "Departamento Pessoal" : [
            "Coordenador",
            "Analista",
            "Assistente",
            "Auxiliar",
        ],
    },
}

st.set_page_config(
    page_title="Controle de Equipamentos de TI",
    page_icon="🖥️",
    layout="wide"
)
st.session_state.setdefault("excluir_id", None)


def _api(method: str, path: str, **kwargs):
    try:
        resp = requests.request(method, f"{API_URL}{path}", timeout=10, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.content else None
    except requests.exceptions.ConnectionError:
        st.error(f"Não foi possível conectar à API em {API_URL}. Ela está rodando?")
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro na API: {e.response.json().get('detail', e)}")
        return None


st.title("🖥️ Controle de Equipamentos de TI")

stats = _api("GET", "/equipamentos/estatisticas") or {}

col_total,col_em_uso,col_manutencao,col_estoque,col_descarte = st.columns(5)
col_total.metric("Total", stats.get("total", 0))
col_em_uso.metric("Em uso", stats.get("em_uso", 0))
col_manutencao.metric("Manutenção", stats.get("manutencao", 0))
col_estoque.metric("Estoque", stats.get("estoque", 0))
col_descarte.metric("Descarte", stats.get("descarte", 0))

st.divider()

with st.expander("➕ Cadastrar novo equipamento", expanded=True):
    # LINHA 01
    col1, col2 = st.columns(2)
    tipo = col1.selectbox(
        "Tipo",
        TIPOS_KEYS,
        format_func=lambda s: TIPOS_LABELS[s],
        placeholder="Selecionar",
        # key="tipo",
    )
    status = col2.selectbox(
        "Status inicial",
        STATUS_KEYS,
        format_func=lambda s: STATUS_LABELS[s],
        placeholder="Selecionar"
    )

    # LINHA 02
    col1, col2, col3 = st.columns(3)
    departamento = col1.selectbox(
        "Departamento",
        options=list(DEPARTAMENTOS.keys()),
        placeholder="Selecionar",
    )
    setores = DEPARTAMENTOS[departamento]
    setor = col2.selectbox(
        label="Setor",
        options=list(setores.keys()),
        placeholder="Selecionar"
    )
    funcoes = setores[setor]
    funcao = col3.selectbox(
        label="Função",
        options=funcoes,
        placeholder="Selecionar"
    )

    # LINHA 03
    col1, col2, col3 = st.columns([3, 1, 1])
    responsavel = col1.text_input("Nome do Responsável")
    identidade = col2.text_input(
        "RG",
        placeholder="Ex: 0000000"
    )
    cpf = col3.text_input(
        "CPF",
        placeholder="Ex: 00000000000"
    )

    with st.form("novo_equipamento", clear_on_submit=True):
        st.markdown(
            body=
            """
                <style>
                    .titulo {
                        margin: 0;
                    }

                    .stDivider {
                        margin: 0;
                    }
                </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            body='<div class="titulo">DADOS DO EQUIPAMENTO</div>',
            unsafe_allow_html=True,
        )
        st.divider()

        # LINHA 01
        col1, col2, col3, col4, col5 = st.columns(5)
        if tipo == "celular":
            MARCAS = MARCAS_CEL
        elif tipo == "computador":
            MARCAS = MARCAS_CPU
        elif tipo == "notebook":
            MARCAS = MARCAS_NTB
        elif tipo == "impressora":
            MARCAS = MARCAS_IMP
        else:
            MARCAS = MARCAS_ROT

        marca = col1.selectbox(
            "Marca",
            MARCAS,
            placeholder="Selecionar",
        )
        modelo = col2.text_input(
            label="Modelo",
            max_chars=150
        )
        serie = col3.text_input(
            label="Número de serie",
            max_chars=20,
        )
        mac = col4.text_input(
            label="MAC",
            max_chars=17,
            placeholder="Ex: 00:00:00:00:00:00"
        )
        sistema = col5.text_input(
            label="Sistema operacional",
            max_chars=20,
        )

        # LINHA 02
        col1, col2, col3 = st.columns(3)
        hd = col1.text_input(
            label="HD",
            max_chars=6,
            placeholder="Ex: 256 GB"
        )
        processador = col2.text_input(
            label="Processador",
            max_chars=100,
        )
        memoria = col3.text_input(
            label="Memória",
            max_chars=6,
            placeholder="Ex: 4 GB"
        )

        # LINHA 03
        if tipo == "celular":
            col1, col2, col3, col4 = st.columns(4)
            operadora = col1.selectbox(
                "Operadora",
                OPERADORAS,
                placeholder="Selecionar"
            )
            linha = col2.text_input(
                label="Número da Linha",
                max_chars=11,
                placeholder="Ex: 81999999999"
            )
            imei1 = col3.text_input(
                label="IMEI 1",
                max_chars=15,
                placeholder="Ex: 000000000000000"
            )
            imei2 = col4.text_input(
                label="IMEI 2",
                max_chars=15,
                placeholder="Ex: 000000000000000"
            )

        # LINHA 04
        col1, col2, col3, col4 = st.columns(4)
        data_aquisicao = col1.date_input(
            label="Data de aquisição",
            value=None,
            format="DD/MM/YYYY",
        )
        data_entrega = col2.date_input(
            label="Data da entrega",
            value=None,
            format="DD/MM/YYYY",
        )
        data_devolucao = col3.date_input(
            label="Data da devolução",
            value=None,
            format="DD/MM/YYYY",
        )
        valor = col4.number_input(
            label="Valor (R$)",
            min_value=0.0,
            step=50.0,
            format="%.2f"
        )
        observacao = st.text_area("Observações")
        enviado = st.form_submit_button("Cadastrar")

        if enviado:
            if not tipo:
                st.warning("Informe o tipo.")
            if not departamento:
                st.warning("Informe o departamento.")
            if not setor:
                st.warning("Informe o setor.")
            if not funcao:
                st.warning("Informe o função.")
            elif not identidade:
                st.warning("Informe o RG do responsável.")
            elif not cpf:
                st.warning("Informe o CPF do responsável.")
            elif not responsavel:
                st.warning("Informe o nome do responsável.")
            elif not marca:
                st.warning("Informe o marca.")
            elif not modelo:
                st.warning("Informe o modelo.")
            elif not serie:
                st.warning("Informe o número de serie.")
            elif not valor:
                st.warning("Informe o valor.")
            else:
                payload = {
                    "tipo": tipo,
                    "status": status,
                    "marca": marca,
                    "modelo": modelo,
                    "serie": serie,
                    "operadora": operadora or None,
                    "linha": linha or None,
                    "imei1": imei1 or None,
                    "imei2": imei2 or None,
                    "identidade": identidade,
                    "cpf": cpf,
                    "responsavel": responsavel,
                    "data_aquisicao": data_aquisicao.isoformat(),
                    "valor": valor,
                    "observacao": observacao or None,
                }
                if _api("POST", "/equipamentos", json=payload) is not None:
                    st.success("Equipamento cadastrado.")
                    st.rerun()

st.subheader("Equipamentos")

col_filtro_tipo, col_filtro_status, col_busca = st.columns([1, 1, 2])
filtro_tipo = col_filtro_tipo.selectbox(
    "Filtrar por tipo",
    ["Todos"] + TIPOS_KEYS,
    format_func=lambda s: "Todos" if s == "Todos" else TIPOS_LABELS[s],
)
filtro_status = col_filtro_status.selectbox(
    "Filtrar por status",
    ["Todos"] + STATUS_KEYS,
    format_func=lambda s: "Todos" if s == "Todos" else STATUS_LABELS[s],
)
busca = col_busca.text_input("Buscar (modelo ou responsável)")

params = {}

if filtro_tipo != "Todos":
    params["tipo"] = filtro_tipo
if filtro_status != "Todos":
    params["status"] = filtro_status
if busca:
    params["q"] = busca

equipamentos = _api("GET", "/equipamentos", params=params) or []

if not equipamentos:
    st.info("Nenhum equipamento encontrado com esses filtros.")

for eq in equipamentos:
    with st.container(border=True):
        col_info, col_status, col_acoes = st.columns([3, 1, 2])
        with col_info:
            st.markdown(f"**{eq['tag']}** · {eq['modelo']}")
            resp_txt = f"com {eq['responsavel']}" if eq["responsavel"] else "sem responsável"
            valor_txt = f"R$ {eq['valor']:.2f}" if eq.get("valor") else "sem valor informado"
            st.caption(f"{resp_txt} · adquirido em {eq['data_aquisicao'] or '—'} · {valor_txt}")
        with col_status:
            st.markdown(f"**{STATUS_LABELS[eq['status']]}**")
        with col_acoes:
            b1, b2, b3 = st.columns(3)
            if b1.button("Movimentar", key=f"mov_{eq['id']}"):
                st.session_state["movimentar_id"] = eq["id"]

            if b2.button("Histórico", key=f"hist_{eq['id']}"):
                st.session_state["historico_id"] = eq["id"]

            if b3.button("Excluir", key=f"del_{eq['id']}"):
                st.session_state["excluir_id"] = eq["id"]

        with st.expander("Documentos", expanded=False):
            st.download_button(
                "Baixar termo de responsabilidade",
                data=gerar_termo_pdf(eq, "responsabilidade"),
                file_name=f"termo_responsabilidade_{eq['tag']}.pdf",
                mime="application/pdf",
                key=f"termo_resp_{eq['id']}",
            )
            st.download_button(
                "Baixar termo de devolução",
                data=gerar_termo_pdf(eq, "devolucao"),
                file_name=f"termo_devolucao_{eq['tag']}.pdf",
                mime="application/pdf",
                key=f"termo_dev_{eq['id']}",
            )

        if st.session_state["excluir_id"] == eq["id"]:
            st.warning(
                f"Excluir {eq['tag']}? Esta ação também removerá o histórico do equipamento."
            )
            confirmar, cancelar = st.columns(2)
            if confirmar.button("Confirmar exclusão", key=f"confirm_del_{eq['id']}"):
                _api("DELETE", f"/equipamentos/{eq['id']}")
                st.session_state["excluir_id"] = None
                st.rerun()
            if cancelar.button("Cancelar", key=f"cancel_del_{eq['id']}"):
                st.session_state["excluir_id"] = None
                st.rerun()

        if st.session_state.get("movimentar_id") == eq["id"]:
            with st.form(f"form_mov_{eq['id']}"):
                novo_resp = st.text_input(
                    "Novo responsável (vazio = devolver ao estoque)", value=eq["responsavel"] or ""
                )
                novo_status = st.selectbox(
                    "Novo status",
                    STATUS_KEYS,
                    index=STATUS_KEYS.index(eq["status"]),
                    format_func=lambda s: STATUS_LABELS[s],
                )
                nota = st.text_input("Observação (opcional)")
                if st.form_submit_button("Confirmar movimentação"):
                    payload = {
                        "responsavel": novo_resp or None,
                        "status": novo_status,
                        "nota": nota or None,
                    }
                    _api("POST", f"/equipamentos/{eq['id']}/movimentar", json=payload)
                    st.session_state["movimentar_id"] = None
                    st.rerun()

        if st.session_state.get("historico_id") == eq["id"]:
            detalhe = _api("GET", f"/equipamentos/{eq['id']}")
            for h in reversed(detalhe.get("historico", [])):
                st.markdown(f"`{h['data'][:10]}` **{h['acao']}** — {h['detalhe']}")
            if st.button("Fechar histórico", key=f"fechar_{eq['id']}"):
                st.session_state["historico_id"] = None
                st.rerun()
