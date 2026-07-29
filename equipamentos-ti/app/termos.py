"""Geração de termos em PDF para movimentação de equipamentos."""

from io import BytesIO
from pathlib import Path
from typing import Literal
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

TermoTipo = Literal["responsabilidade", "devolucao"]


def _registrar_fontes() -> None:
    if "Vera" in pdfmetrics.getRegisteredFontNames():
        return
    pasta_fontes = Path(reportlab.__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("Vera", str(pasta_fontes / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("Vera-Bold", str(pasta_fontes / "VeraBd.ttf")))


def _texto_termo(tipo: TermoTipo) -> str:
    if tipo == "responsabilidade":
        return (
            "Declaro que recebi o equipamento descrito neste documento e assumo, "
            "a partir desta data, a responsabilidade por sua guarda, conservação "
            "e utilização exclusiva para fins de trabalho. Comprometo-me a comunicar "
            "imediatamente qualquer dano, perda, furto ou necessidade de manutenção."
        )
    return (
        "Declaro que devolvi o equipamento descrito neste documento ao setor de TI. "
        "O item será conferido quanto ao seu estado de conservação, acessórios e "
        "condições de funcionamento."
    )


def gerar_termo_pdf(equipamento: dict, tipo: TermoTipo) -> bytes:
    """Retorna um PDF de responsabilidade ou devolução para um equipamento."""
    _registrar_fontes()
    responsavel = equipamento.get("responsavel") or "Não informado"
    titulo = (
        "TERMO DE RESPONSABILIDADE"
        if tipo == "responsabilidade"
        else "TERMO DE DEVOLUÇÃO DE EQUIPAMENTO"
    )
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=titulo,
        author="Controle de Equipamentos de TI",
    )

    estilos = getSampleStyleSheet()
    titulo_estilo = ParagraphStyle(
        "TermoTitulo",
        parent=estilos["Title"],
        alignment=TA_CENTER,
        fontName="Vera-Bold",
        fontSize=15,
        leading=19,
        spaceAfter=10,
    )
    corpo_estilo = ParagraphStyle(
        "TermoCorpo",
        parent=estilos["BodyText"],
        fontName="Vera",
        fontSize=10.5,
        leading=16,
        spaceAfter=12,
    )
    rotulo_estilo = ParagraphStyle(
        "Rotulo",
        parent=corpo_estilo,
        fontName="Vera-Bold",
        spaceAfter=0,
    )
    valor_estilo = ParagraphStyle("Valor", parent=corpo_estilo, spaceAfter=0)

    dados = [
        [
            Paragraph("Tag", rotulo_estilo),
            Paragraph(escape(str(equipamento["tag"])), valor_estilo),
        ],
        [
            Paragraph("Tipo", rotulo_estilo),
            Paragraph(escape(str(equipamento["tipo"])), valor_estilo),
        ],
        [
            Paragraph("Modelo", rotulo_estilo),
            Paragraph(escape(str(equipamento["modelo"])), valor_estilo),
        ],
        [Paragraph("Responsável", rotulo_estilo), Paragraph(escape(responsavel), valor_estilo)],
        [
            Paragraph("Status", rotulo_estilo),
            Paragraph(escape(str(equipamento.get("status", "Não informado"))), valor_estilo),
        ],
    ]
    tabela = Table(dados, colWidths=[4.2 * cm, 12.1 * cm], hAlign="LEFT")
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8EEF5")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAB7C4")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#C8D1DA")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    historia = [
        Paragraph(
            "CONTROLE DE EQUIPAMENTOS DE TI",
            ParagraphStyle("Cabecalho", parent=corpo_estilo, fontName="Vera-Bold"),
        ),
        Spacer(1, 0.3 * cm),
        Paragraph(titulo, titulo_estilo),
        HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#2B5B84")),
        Spacer(1, 0.5 * cm),
        tabela,
        Spacer(1, 0.7 * cm),
        Paragraph(_texto_termo(tipo), corpo_estilo),
        Spacer(1, 1.8 * cm),
        HRFlowable(width="45%", thickness=0.6, color=colors.black, hAlign="CENTER"),
        Paragraph(
            "Assinatura do responsável",
            ParagraphStyle("Assinatura", parent=corpo_estilo, alignment=TA_CENTER),
        ),
        Spacer(1, 0.9 * cm),
        Paragraph("Data: ____ / ____ / ______", corpo_estilo),
    ]
    documento.build(historia)
    return buffer.getvalue()
