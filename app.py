from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Dashboard de Chamados | SLA e Operação",
    page_icon="📊",
    layout="wide",
)

CUSTOM_CSS = """
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
}

html, body, [class*="css"] {
    color: #0F172A;
}

.main-title {
    font-size: 2.15rem;
    font-weight: 900;
    line-height: 1.25;
    margin-top: 0.6rem;
    margin-bottom: 0.35rem;
    color: #0F172A;
}

.sub-title {
    font-size: 1rem;
    color: #334155;
    margin-bottom: 1.4rem;
    font-weight: 500;
}

.kpi-card {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 6px solid #475569;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.10);
    padding: 18px 16px 16px 16px;
    min-height: 145px;
}

.kpi-card.good {
    background: #ECFDF5;
    border-color: #86EFAC;
    border-left-color: #059669;
}

.kpi-card.bad {
    background: #FEF2F2;
    border-color: #FCA5A5;
    border-left-color: #DC2626;
}

.kpi-label {
    font-size: 0.76rem;
    color: #334155;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .055rem;
    text-align: center;
}

.kpi-value {
    font-size: 2rem;
    color: #020617;
    font-weight: 900;
    line-height: 1.2;
    text-align: center;
    margin-top: 8px;
}

.kpi-help {
    font-size: 0.82rem;
    color: #334155;
    text-align: center;
    margin-top: 8px;
    font-weight: 600;
}

.kpi-help.good-text {
    color: #047857;
    font-weight: 800;
}

.kpi-help.bad-text {
    color: #B91C1C;
    font-weight: 800;
}

.kpi-delta-wrap {
    text-align: center;
    margin-top: 9px;
}

.kpi-delta {
    font-size: 0.78rem;
    text-align: center;
    font-weight: 900;
    padding: 5px 9px;
    border-radius: 999px;
    display: inline-block;
}

.kpi-delta.positive {
    color: #047857;
    background: #D1FAE5;
}

.kpi-delta.negative {
    color: #B91C1C;
    background: #FEE2E2;
}

.kpi-delta.neutral {
    color: #1D4ED8;
    background: #DBEAFE;
}

.section-divider {
    border: 0;
    border-top: 1px solid #CBD5E1;
    margin: 2.1rem 0 1.7rem 0;
}

.note-box {
    border-left: 5px solid #2563EB;
    background: #EFF6FF;
    border-radius: 10px;
    padding: 15px 18px;
    margin-top: 18px;
    color: #0F172A;
    font-weight: 500;
}

.alert-box {
    border-left: 5px solid #DC2626;
    background: #FEF2F2;
    border-radius: 10px;
    padding: 15px 18px;
    margin-top: 18px;
    color: #0F172A;
    font-weight: 500;
}

.small-muted {
    color: #334155;
    font-size: 0.92rem;
    font-weight: 500;
}

.chart-title {
    font-size: 1.05rem;
    font-weight: 900;
    color: #0F172A;
    margin-top: 0.2rem;
    margin-bottom: 0.15rem;
}

.chart-subtitle {
    font-size: 0.88rem;
    color: #334155;
    margin-bottom: 0.4rem;
    font-weight: 500;
}

.section-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 14px;
    padding: 16px 16px 8px 16px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.08);
    margin-top: 14px;
    margin-bottom: 20px;
}

.evo-card {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 14px;
    padding: 15px 14px 13px 14px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.08);
    border-left: 5px solid #2563EB;
    margin-bottom: 14px;
}

.evo-card.good {
    border-left-color: #059669;
    background: #F0FDF4;
}

.evo-card.bad {
    border-left-color: #DC2626;
    background: #FEF2F2;
}

.evo-card.neutral {
    border-left-color: #2563EB;
    background: #EFF6FF;
}

.evo-label {
    font-size: 0.82rem;
    color: #334155;
    font-weight: 800;
    margin-bottom: 8px;
}

.evo-value {
    font-size: 1.75rem;
    color: #020617;
    font-weight: 900;
    line-height: 1.1;
}

.evo-delta {
    font-size: 0.78rem;
    font-weight: 900;
    margin-top: 8px;
    display: inline-block;
    padding: 4px 8px;
    border-radius: 999px;
}

.evo-delta.positive {
    color: #047857;
    background: #D1FAE5;
}

.evo-delta.negative {
    color: #B91C1C;
    background: #FEE2E2;
}

.evo-delta.neutral {
    color: #1D4ED8;
    background: #DBEAFE;
}

h1, h2, h3 {
    color: #0F172A !important;
    font-weight: 900 !important;
}

p, span, label {
    color: #0F172A;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

COL_ALIASES = {
    "numero": ["N", "Número", "Numero", "Nº", "N°"],
    "abertura": ["Abertura", "Data Abertura", "Data de Abertura"],
    "primeiro_retorno": ["1 Retorno", "1º Retorno", "Primeiro Retorno", "Primeiro retorno"],
    "empresa": ["Empresa", "Cliente", "Razão Social", "Razao Social"],
    "responsavel": ["Responsável", "Responsavel", "Atendente", "Técnico", "Tecnico"],
    "setor": ["Setor de Atendimento", "Setor", "Departamento"],
    "tipo": ["Tipo"],
    "item": ["Item"],
    "vencimento": ["Vencimento", "Data Vencimento"],
    "encerramento": ["Encerramento", "Data Encerramento", "Fechamento"],
    "status": ["Status"],
    "categoria": ["Categoria"],
    "situacao": ["Situação", "Situa??o", "Situacao"],
}

INDICATORS = [
    "Total de chamados",
    "Dentro SLA",
    "Fora SLA",
    "Tratados até 72h",
    "Tratados acima de 72h",
    "Em aberto / sem encerramento",
    "Backlog por status",
    "Empresas",
    "FCR tratado",
    "First Call Resolution até 1h",
    "Resolvidos acima de 1h",
    "% SLA",
    "% FCR 1h",
    "% 1º retorno até 1h",
]

COLOR_MAP_MONTHS = ["#2563EB", "#F97316"]

PLOT_FONT = dict(family="Arial", size=13, color="#0F172A")


def find_col(df: pd.DataFrame, key: str) -> Optional[str]:
    aliases = COL_ALIASES.get(key, [])
    normalized_columns = {str(col).strip().lower(): col for col in df.columns}
    for alias in aliases:
        col = normalized_columns.get(alias.strip().lower())
        if col is not None:
            return col
    return None


def series_or_empty(df: pd.DataFrame, key: str) -> pd.Series:
    col = find_col(df, key)
    if col is None:
        return pd.Series([pd.NA] * len(df), index=df.index)
    return df[col]


def clean_text_value(value: Any) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    text = " ".join(text.split())
    return text


def normalize_empresa_name(value: Any) -> str:
    text = clean_text_value(value)
    if not text:
        return ""

    upper = text.upper()
    compact = upper.replace(".", " ").replace("-", " ").replace("_", " ").replace("/", " ")
    compact = " ".join(compact.split())

    if "CBLOC" in compact or "C BLOC" in compact or "CBLOC BRASIL" in compact or "CBLO" in compact:
        return "CBLOC BRASIL LOCAÇÃO DE EQUIPAMENTOS"

    return text


def normalize_dimension_value(value: Any, key: str) -> str:
    text = clean_text_value(value)
    if not text:
        return ""
    if key == "empresa":
        return normalize_empresa_name(text)
    return text


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(how="all")
    df.columns = [str(c).strip() if str(c) != "nan" else "" for c in df.columns]

    numero_col = find_col(df, "numero")
    if numero_col:
        df = df[df[numero_col].notna()]

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "NaT": pd.NA, "None": pd.NA})

    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def read_excel_smart(uploaded_file: Any) -> pd.DataFrame:
    if uploaded_file is None:
        return pd.DataFrame()

    try:
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file)
    except Exception:
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file, engine="xlrd")

    return clean_dataframe(df)


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, dayfirst=True, errors="coerce")


def count_leq_hours(start: pd.Series, end: pd.Series, hours: float) -> int:
    delta_hours = (end - start).dt.total_seconds() / 3600
    return int(((delta_hours <= hours) & end.notna() & start.notna()).sum())


def count_gt_hours(start: pd.Series, end: pd.Series, hours: float) -> int:
    delta_hours = (end - start).dt.total_seconds() / 3600
    return int(((delta_hours > hours) & end.notna() & start.notna()).sum())


def pct(numerator: float, denominator: float) -> float:
    if denominator == 0 or pd.isna(denominator):
        return 0.0
    return float(numerator) / float(denominator) * 100


def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
    if df.empty:
        return {}

    abertura = to_datetime(series_or_empty(df, "abertura"))
    primeiro_retorno = to_datetime(series_or_empty(df, "primeiro_retorno"))
    vencimento = to_datetime(series_or_empty(df, "vencimento"))
    encerramento = to_datetime(series_or_empty(df, "encerramento"))
    status = series_or_empty(df, "status").astype(str)
    empresa = series_or_empty(df, "empresa")

    total = int(len(df))
    encerrados_mask = encerramento.notna()
    fcr_tratado = int(encerrados_mask.sum())

    dentro_sla = int(((encerramento <= vencimento) & encerrados_mask & vencimento.notna()).sum())
    fora_sla = int(((encerramento > vencimento) & encerrados_mask & vencimento.notna()).sum())
    base_sla = dentro_sla + fora_sla

    tratados_ate_72h = count_leq_hours(abertura, encerramento, 72)
    tratados_acima_72h = count_gt_hours(abertura, encerramento, 72)
    sem_encerramento = int(encerramento.isna().sum())

    status_encerrado = status.str.contains("Encerrada", case=False, na=False)
    backlog_status = int((~status_encerrado).sum())

    fcr_ate_1h = count_leq_hours(abertura, encerramento, 1)
    resolvidos_acima_1h = count_gt_hours(abertura, encerramento, 1)
    primeiro_retorno_ate_1h = count_leq_hours(abertura, primeiro_retorno, 1)

    empresas_unicas = empresa.dropna().map(normalize_empresa_name).replace("", pd.NA).dropna().nunique()

    return {
        "Total de chamados": total,
        "Dentro SLA": dentro_sla,
        "Fora SLA": fora_sla,
        "% SLA": pct(dentro_sla, base_sla),
        "Tratados até 72h": tratados_ate_72h,
        "Tratados acima de 72h": tratados_acima_72h,
        "Em aberto / sem encerramento": sem_encerramento,
        "Backlog por status": backlog_status,
        "Empresas": int(empresas_unicas),
        "FCR tratado": fcr_tratado,
        "First Call Resolution até 1h": fcr_ate_1h,
        "Resolvidos acima de 1h": resolvidos_acima_1h,
        "% FCR 1h": pct(fcr_ate_1h, fcr_tratado),
        "% 1º retorno até 1h": pct(primeiro_retorno_ate_1h, total),
    }


def format_int(value: float) -> str:
    return f"{int(round(value)):,}".replace(",", ".")


def format_pct(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}%".replace(".", ",")


def format_pp(value: float) -> str:
    return f"{value:+.1f}".replace(".", ",") + " p.p."


def format_metric(indicator: str, value: float) -> str:
    if indicator.startswith("%"):
        return format_pct(value)
    return format_int(value)


def delta_direction_class(indicator: str, diff: float) -> str:
    if diff == 0:
        return "neutral"

    good_when_up = [
        "Dentro SLA",
        "% SLA",
        "Tratados até 72h",
        "Empresas",
        "First Call Resolution até 1h",
        "% FCR 1h",
        "% 1º retorno até 1h",
        "FCR tratado",
    ]

    good_when_down = [
        "Fora SLA",
        "Tratados acima de 72h",
        "Em aberto / sem encerramento",
        "Backlog por status",
    ]

    neutral_indicators = ["Total de chamados", "Resolvidos acima de 1h"]

    if indicator in neutral_indicators:
        return "neutral"
    if indicator in good_when_up:
        return "positive" if diff > 0 else "negative"
    if indicator in good_when_down:
        return "positive" if diff < 0 else "negative"
    return "positive" if diff > 0 else "negative"


def delta_text(indicator: str, current_value: float, previous_value: float, previous_label: str) -> str:
    diff = current_value - previous_value
    arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"

    if indicator.startswith("%"):
        return f"{arrow} {format_pp(diff)} vs {previous_label}"

    if previous_value:
        variation = pct(diff, previous_value)
        return f"{arrow} {int(diff):+d} | {format_pct(variation)} vs {previous_label}"

    return f"{arrow} {int(diff):+d} vs {previous_label}"


def kpi_delta_html(
    indicator: str,
    current_value: float,
    previous_value: float,
    previous_label: str,
) -> str:
    diff = current_value - previous_value
    delta_class = delta_direction_class(indicator, diff)
    text = delta_text(indicator, current_value, previous_value, previous_label)
    return f'<span class="kpi-delta {delta_class}">{text}</span>'


def kpi_card(
    label: str,
    value: str,
    help_text: str,
    status: str = "neutral",
    delta_html: str = "",
) -> None:
    css_class = "good" if status == "good" else "bad" if status == "bad" else ""
    help_class = "good-text" if status == "good" else "bad-text" if status == "bad" else ""
    delta_block = f'<div class="kpi-delta-wrap">{delta_html}</div>' if delta_html else ""

    html = (
        f'<div class="kpi-card {css_class}">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-help {help_class}">{help_text}</div>'
        f'{delta_block}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def build_comparison(previous: Dict[str, float], current: Dict[str, float]) -> pd.DataFrame:
    rows = []
    for indicator in INDICATORS:
        prev = float(previous.get(indicator, 0))
        curr = float(current.get(indicator, 0))
        diff = curr - prev
        variation = pct(diff, prev) if prev else 0.0
        rows.append(
            {
                "Indicador": indicator,
                "Mês anterior": prev,
                "Mês atual": curr,
                "Diferença": diff,
                "Variação %": variation,
                "Tipo": "Percentual" if indicator.startswith("%") else "Quantidade",
            }
        )
    return pd.DataFrame(rows)


def display_comparison_table(comp: pd.DataFrame) -> None:
    formatted_rows = []
    for _, row in comp.iterrows():
        is_pct = row["Tipo"] == "Percentual"
        formatted_rows.append(
            {
                "Indicador": row["Indicador"],
                "Mês anterior": format_pct(row["Mês anterior"], 1) if is_pct else format_int(row["Mês anterior"]),
                "Mês atual": format_pct(row["Mês atual"], 1) if is_pct else format_int(row["Mês atual"]),
                "Diferença": format_pp(row["Diferença"]) if is_pct else f"{int(row['Diferença']):+d}",
                "Variação %": format_pct(row["Variação %"], 1),
            }
        )
    st.dataframe(pd.DataFrame(formatted_rows), use_container_width=True, hide_index=True)


def current_overview_table(current: Dict[str, float]) -> pd.DataFrame:
    rows = [
        ("Total de chamados", format_int(current["Total de chamados"]), "Total de chamados recebidos no mês."),
        ("Dentro SLA", format_int(current["Dentro SLA"]), "Atendimentos encerrados dentro do prazo contratado."),
        ("Fora SLA", format_int(current["Fora SLA"]), "Chamados encerrados em atraso com risco de estouro nos prazos."),
        ("% SLA", format_pct(current["% SLA"]), "Percentual de atendimento dentro do SLA considerando chamados encerrados."),
        ("Tratados até 72h", format_int(current["Tratados até 72h"]), "Chamados concluídos em tempo satisfatório."),
        ("Tratados acima de 72h", format_int(current["Tratados acima de 72h"]), "Chamados com ciclo longo de resolução, acima de 72h."),
        ("Em aberto / sem encerramento", format_int(current["Em aberto / sem encerramento"]), "Chamados sem data de encerramento registrada."),
        ("Backlog por status", format_int(current["Backlog por status"]), "Chamados cujo status ainda não está como encerrado."),
        ("Empresas", format_int(current["Empresas"]), "Volume de clientes únicos atendidos no período."),
        ("FCR tratado", format_int(current["FCR tratado"]), "Total de chamados com encerramento válido."),
        ("First Call Resolution até 1h", format_int(current["First Call Resolution até 1h"]), "Chamados resolvidos em até 1 hora."),
        ("% FCR 1h", format_pct(current["% FCR 1h"]), "Percentual de chamados encerrados em até 1 hora."),
        ("% 1º retorno até 1h", format_pct(current["% 1º retorno até 1h"]), "Percentual de chamados com primeiro retorno em até 1 hora."),
    ]
    return pd.DataFrame(rows, columns=["Indicador", "Valor", "Observação"])


def truncate_label(text: str, max_len: int = 30) -> str:
    text = clean_text_value(text)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def count_dimension(df: pd.DataFrame, key: str) -> pd.Series:
    col = find_col(df, key)
    if col is None or df.empty:
        return pd.Series(dtype="int64")

    numero_col = find_col(df, "numero")
    temp = pd.DataFrame()
    temp["Nome"] = df[col].map(lambda value: normalize_dimension_value(value, key))
    temp = temp[temp["Nome"] != ""]

    if numero_col:
        temp["Chamado"] = df[numero_col].astype(str).map(clean_text_value)
        temp = temp[temp["Chamado"] != ""]
        return temp.groupby("Nome")["Chamado"].nunique().sort_values(ascending=False)

    return temp["Nome"].value_counts().sort_values(ascending=False)


def top_table(df: pd.DataFrame, key: str, top_n: int = 5, include_other: bool = False) -> pd.DataFrame:
    counts = count_dimension(df, key)
    if counts.empty:
        return pd.DataFrame(columns=["Nome", "Quantidade", "% do total", "Nome curto"])

    total_base = int(counts.sum()) if int(counts.sum()) else 1
    top_counts = counts.head(top_n).copy()

    if include_other and len(counts) > top_n:
        top_counts.loc["Outros"] = counts.iloc[top_n:].sum()

    table = pd.DataFrame({"Nome": top_counts.index, "Quantidade": top_counts.values})
    table["% do total"] = [format_pct(pct(v, total_base), 1) for v in table["Quantidade"]]
    table["Nome curto"] = [
        "Outros" if nome == "Outros" else f"{idx + 1}. {truncate_label(nome, 28)}"
        for idx, nome in enumerate(table["Nome"])
    ]
    return table


def compare_dimension(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    key: str,
    previous_label: str,
    current_label: str,
    top_n: int = 10,
) -> pd.DataFrame:
    prev_counts = count_dimension(previous_df, key)
    curr_counts = count_dimension(current_df, key)

    if prev_counts.empty and curr_counts.empty:
        return pd.DataFrame(columns=["Nome", "Nome curto", previous_label, current_label, "Diferença", "Total"])

    total_counts = prev_counts.add(curr_counts, fill_value=0).sort_values(ascending=False)
    selected_names = total_counts.head(top_n).index.tolist()
    rows = []

    for idx, name in enumerate(selected_names):
        prev = int(prev_counts.get(name, 0))
        curr = int(curr_counts.get(name, 0))
        diff = curr - prev
        rows.append(
            {
                "Nome": name,
                "Nome curto": f"{idx + 1}. {truncate_label(name, 30)}",
                previous_label: prev,
                current_label: curr,
                "Diferença": diff,
                "Total": prev + curr,
            }
        )

    return pd.DataFrame(rows)


def pain_points(current: Dict[str, float]) -> pd.DataFrame:
    rows = []

    def add(indicator: str, value: str, is_critical: bool, reading: str) -> None:
        rows.append(
            {
                "Dor / Indicador": indicator,
                "Mês atual": value,
                "Status": "Crítico" if is_critical else "Bom",
                "Leitura executiva": reading,
            }
        )

    add(
        "% Dentro do SLA",
        format_pct(current["% SLA"]),
        current["% SLA"] < 80,
        "Cumprimento de SLA dentro da meta recomendada." if current["% SLA"] >= 80 else "SLA abaixo da meta recomendada.",
    )
    add(
        "Backlog por status",
        format_int(current["Backlog por status"]),
        current["Backlog por status"] > 0,
        f"Backlog elevado ({format_int(current['Backlog por status'])} chamados ativos).",
    )
    add(
        "% 1º retorno até 1h",
        format_pct(current["% 1º retorno até 1h"]),
        current["% 1º retorno até 1h"] < 70,
        "Agilidade de primeiro retorno abaixo da meta de 70%.",
    )
    add(
        "Fora do SLA",
        format_int(current["Fora SLA"]),
        current["Fora SLA"] > 0,
        f"Volume considerável de chamados fora do SLA ({format_int(current['Fora SLA'])}).",
    )
    add(
        "Tratados acima de 72h",
        format_int(current["Tratados acima de 72h"]),
        current["Tratados acima de 72h"] > 0,
        f"Volume elevado de chamados resolvidos acima de 72h ({format_int(current['Tratados acima de 72h'])}).",
    )
    add(
        "Sem encerramento registrado",
        format_int(current["Em aberto / sem encerramento"]),
        current["Em aberto / sem encerramento"] > 0,
        f"Chamados sem encerramento registrado ({format_int(current['Em aberto / sem encerramento'])}).",
    )
    return pd.DataFrame(rows)


def render_kpis(
    current: Dict[str, float],
    previous: Optional[Dict[str, float]] = None,
    current_label: str = "Mês atual",
    previous_label: str = "Mês anterior",
) -> None:
    def delta(indicator: str) -> str:
        if previous is None:
            return ""
        return kpi_delta_html(indicator, current[indicator], previous[indicator], previous_label)

    kpi_cols = st.columns(5)

    with kpi_cols[0]:
        kpi_card(
            "Total de chamados",
            format_int(current["Total de chamados"]),
            f"Visão de {current_label}",
            "neutral",
            delta("Total de chamados"),
        )

    with kpi_cols[1]:
        sla_status = "good" if current["% SLA"] >= 80 else "bad"
        kpi_card("% Dentro do SLA", format_pct(current["% SLA"]), "Meta: ≥ 80%", sla_status, delta("% SLA"))

    with kpi_cols[2]:
        retorno_status = "good" if current["% 1º retorno até 1h"] >= 70 else "bad"
        kpi_card(
            "% 1º retorno até 1h",
            format_pct(current["% 1º retorno até 1h"]),
            "Meta: ≥ 70%",
            retorno_status,
            delta("% 1º retorno até 1h"),
        )

    with kpi_cols[3]:
        status = "bad" if current["Backlog por status"] > 0 else "good"
        kpi_card(
            "Backlog por status",
            format_int(current["Backlog por status"]),
            "Sem encerr. / status",
            status,
            delta("Backlog por status"),
        )

    with kpi_cols[4]:
        status = "bad" if current["Tratados acima de 72h"] > 0 else "good"
        kpi_card(
            "Tratados acima de 72h",
            format_int(current["Tratados acima de 72h"]),
            "Encerrados > 72h",
            status,
            delta("Tratados acima de 72h"),
        )


def render_evolution_card(
    label: str,
    indicator: str,
    current: Dict[str, float],
    previous: Dict[str, float],
    previous_label: str,
) -> None:
    current_value = current[indicator]
    previous_value = previous[indicator]
    diff = current_value - previous_value
    delta_class = delta_direction_class(indicator, diff)
    delta_label = delta_text(indicator, current_value, previous_value, previous_label)
    card_class = delta_class

    st.markdown(
        f'<div class="evo-card {card_class}">'
        f'<div class="evo-label">{label}</div>'
        f'<div class="evo-value">{format_metric(indicator, current_value)}</div>'
        f'<div class="evo-delta {delta_class}">{delta_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_evolution_cards(
    previous: Dict[str, float],
    current: Dict[str, float],
    previous_label: str,
    current_label: str,
) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header(f"Resumo da evolução | {previous_label} x {current_label}")
    st.markdown(
        '<div class="small-muted">Cards executivos com os mesmos indicadores usados nos gráficos de comparação.</div>',
        unsafe_allow_html=True,
    )

    cards = [
        ("Chamados no mês atual", "Total de chamados"),
        ("Dentro SLA atual", "Dentro SLA"),
        ("Fora SLA atual", "Fora SLA"),
        ("% SLA atual", "% SLA"),
        ("Até 72h atual", "Tratados até 72h"),
        ("Acima 72h atual", "Tratados acima de 72h"),
        ("Em aberto atual", "Em aberto / sem encerramento"),
        ("Empresas atual", "Empresas"),
        ("FCR até 1h atual", "First Call Resolution até 1h"),
        ("% FCR 1h atual", "% FCR 1h"),
    ]

    for start in range(0, len(cards), 5):
        row_cards = cards[start:start + 5]
        cols = st.columns(5)
        for col, (label, indicator) in zip(cols, row_cards):
            with col:
                render_evolution_card(label, indicator, current, previous, previous_label)


def render_vertical_chart(
    chart_df: pd.DataFrame,
    indicator_map: Dict[str, str],
    title: str,
    subtitle: str,
    previous_label: str,
    current_label: str,
    y_title: str,
    is_percentage: bool = False,
    height: int = 390,
) -> None:
    indicators = list(indicator_map.keys())
    filtered = chart_df[chart_df["Indicador"].isin(indicators)].copy()
    filtered["Indicador curto"] = filtered["Indicador"].map(indicator_map)
    filtered["Indicador curto"] = pd.Categorical(
        filtered["Indicador curto"], categories=list(indicator_map.values()), ordered=True
    )
    filtered = filtered.sort_values("Indicador curto")

    long_df = filtered.melt(
        id_vars=["Indicador", "Indicador curto"],
        value_vars=[previous_label, current_label],
        var_name="Mês",
        value_name="Valor",
    )

    st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-subtitle">{subtitle}</div>', unsafe_allow_html=True)

    max_value = max(float(long_df["Valor"].max()), 10.0)

    fig = px.bar(
        long_df,
        x="Indicador curto",
        y="Valor",
        color="Mês",
        barmode="group",
        text="Valor",
        color_discrete_sequence=COLOR_MAP_MONTHS,
    )

    if is_percentage:
        fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
        y_range = [0, max_value + 15]
    else:
        fig.update_traces(texttemplate="%{y:.0f}", textposition="outside")
        y_range = [0, max_value * 1.18]

    fig.update_layout(
        height=height,
        xaxis_title="",
        yaxis_title=y_title,
        legend_title="",
        font=PLOT_FONT,
        yaxis_range=y_range,
        margin=dict(l=10, r=10, t=20, b=70),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )
    fig.update_xaxes(tickangle=-25, tickfont=dict(size=11, color="#0F172A"))
    fig.update_yaxes(tickfont=dict(size=11, color="#0F172A"), gridcolor="#E5E7EB")

    st.plotly_chart(fig, use_container_width=True)


def render_comparison_charts(
    previous: Dict[str, float],
    current: Dict[str, float],
    previous_label: str,
    current_label: str,
) -> pd.DataFrame:
    comp = build_comparison(previous, current)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Comparação entre mês anterior e mês atual")
    st.markdown(
        f'<div class="small-muted">Gráficos de barras verticais usando os mesmos indicadores do resumo acima. Ordem: {previous_label} x {current_label}.</div>',
        unsafe_allow_html=True,
    )

    chart_df = comp.rename(columns={"Mês anterior": previous_label, "Mês atual": current_label})
    col1, col2, col3 = st.columns(3)

    with col1:
        render_vertical_chart(
            chart_df,
            {"Total de chamados": "Chamados", "Dentro SLA": "Dentro SLA", "Fora SLA": "Fora SLA"},
            "Volume geral",
            "Chamados recebidos e resultado de SLA.",
            previous_label,
            current_label,
            "Quantidade",
            is_percentage=False,
            height=390,
        )

    with col2:
        render_vertical_chart(
            chart_df,
            {
                "Tratados até 72h": "Até 72h",
                "Tratados acima de 72h": "Acima 72h",
                "Em aberto / sem encerramento": "Em aberto",
            },
            "Tratativas",
            "Tempo de resolução e chamados sem encerramento.",
            previous_label,
            current_label,
            "Quantidade",
            is_percentage=False,
            height=390,
        )

    with col3:
        render_vertical_chart(
            chart_df,
            {
                "Empresas": "Empresas",
                "First Call Resolution até 1h": "FCR até 1h",
                "FCR tratado": "FCR tratado",
            },
            "Produtividade",
            "Empresas atendidas, FCR tratado e resoluções rápidas.",
            previous_label,
            current_label,
            "Quantidade",
            is_percentage=False,
            height=390,
        )

    render_vertical_chart(
        chart_df,
        {"% SLA": "% SLA", "% FCR 1h": "% FCR 1h", "% 1º retorno até 1h": "% 1º retorno"},
        "Indicadores percentuais",
        "Comparação percentual entre mês anterior e mês atual.",
        previous_label,
        current_label,
        "Percentual (%)",
        is_percentage=True,
        height=390,
    )

    return comp


def render_comparison_table_and_reading(comp: pd.DataFrame, previous_label: str, current_label: str) -> None:
    with st.expander("Ver tabela detalhada da comparação"):
        display_comparison_table(comp)

    total_row = comp.loc[comp["Indicador"] == "Total de chamados"].iloc[0]
    sla_row = comp.loc[comp["Indicador"] == "% SLA"].iloc[0]
    fcr_row = comp.loc[comp["Indicador"] == "% FCR 1h"].iloc[0]

    st.markdown(
        f"""
        <div class='note-box'>
        <b>Leitura da evolução:</b> de {previous_label} para {current_label}, o volume variou
        <b>{int(total_row['Diferença']):+d} chamados</b> ({format_pct(total_row['Variação %'])}).
        O SLA mudou <b>{format_pp(sla_row['Diferença'])}</b> e o FCR até 1h mudou
        <b>{format_pp(fcr_row['Diferença'])}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_current_overview(current: Dict[str, float], current_label: str) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header(f"Comparativo geral do mês atual | {current_label}")
    st.dataframe(current_overview_table(current), use_container_width=True, hide_index=True)


def render_pie_chart_from_table(table: pd.DataFrame, title: str, height: int = 340, hole: float = 0.45) -> None:
    if table.empty:
        st.info("Dados não encontrados para este gráfico.")
        return

    fig = px.pie(
        table,
        names="Nome curto",
        values="Quantidade",
        title=title,
        hole=hole,
        color_discrete_sequence=px.colors.qualitative.Bold,
        hover_data=["Nome", "% do total"],
    )
    fig.update_traces(textinfo="percent+label", textfont_size=11, marker=dict(line=dict(color="#FFFFFF", width=2)))
    fig.update_layout(
        height=height,
        font=PLOT_FONT,
        title_font=dict(size=16, color="#0F172A"),
        legend_font=dict(size=10, color="#0F172A"),
        margin=dict(l=5, r=5, t=45, b=5),
        paper_bgcolor="#FFFFFF",
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_horizontal_bar_from_table(table: pd.DataFrame, title: str, height: int = 330) -> None:
    if table.empty:
        st.info("Dados não encontrados para este gráfico.")
        return

    chart_table = table.sort_values("Quantidade", ascending=False).copy()
    fig = px.bar(
        chart_table,
        x="Quantidade",
        y="Nome curto",
        orientation="h",
        text="Quantidade",
        title=title,
        hover_data=["Nome", "% do total"],
        color_discrete_sequence=["#2563EB"],
    )
    fig.update_traces(texttemplate="%{x:.0f}", textposition="outside")
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10, color="#0F172A"), title="")
    fig.update_xaxes(title="Quantidade", tickfont=dict(size=10, color="#0F172A"), gridcolor="#E5E7EB")
    fig.update_layout(
        height=height,
        font=PLOT_FONT,
        title_font=dict(size=16, color="#0F172A"),
        margin=dict(l=5, r=45, t=45, b=25),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_dimension_comparison_bar(
    table: pd.DataFrame,
    title: str,
    previous_label: str,
    current_label: str,
    height: int = 360,
) -> None:
    if table.empty:
        st.info("Dados não encontrados para comparação.")
        return

    long_df = table.melt(
        id_vars=["Nome", "Nome curto", "Diferença", "Total"],
        value_vars=[previous_label, current_label],
        var_name="Mês",
        value_name="Quantidade",
    )

    fig = px.bar(
        long_df,
        x="Quantidade",
        y="Nome curto",
        color="Mês",
        orientation="h",
        barmode="group",
        text="Quantidade",
        title=title,
        hover_data=["Nome"],
        color_discrete_sequence=COLOR_MAP_MONTHS,
    )
    fig.update_traces(texttemplate="%{x:.0f}", textposition="outside")
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10, color="#0F172A"), title="")
    fig.update_xaxes(title="Quantidade", tickfont=dict(size=10, color="#0F172A"), gridcolor="#E5E7EB")
    fig.update_layout(
        height=height,
        font=PLOT_FONT,
        title_font=dict(size=16, color="#0F172A"),
        legend_title="",
        margin=dict(l=5, r=50, t=50, b=25),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_dimension_comparison(
    previous_df: pd.DataFrame,
    current_df: pd.DataFrame,
    previous_label: str,
    current_label: str,
) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header(f"Comparativo por dimensão | {previous_label} x {current_label}")
    st.markdown(
        '<div class="small-muted">Comparação dos principais clientes, setores, responsáveis, categorias e itens entre os dois meses.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        clientes = compare_dimension(previous_df, current_df, "empresa", previous_label, current_label, top_n=10)
        render_dimension_comparison_bar(clientes, f"Clientes | {previous_label} x {current_label}", previous_label, current_label, height=380)
    with col2:
        setores = compare_dimension(previous_df, current_df, "setor", previous_label, current_label, top_n=8)
        render_dimension_comparison_bar(setores, f"Setores | {previous_label} x {current_label}", previous_label, current_label, height=380)

    col3, col4 = st.columns(2)
    with col3:
        responsaveis = compare_dimension(previous_df, current_df, "responsavel", previous_label, current_label, top_n=10)
        render_dimension_comparison_bar(responsaveis, f"Responsáveis | {previous_label} x {current_label}", previous_label, current_label, height=380)
    with col4:
        categorias = compare_dimension(previous_df, current_df, "categoria", previous_label, current_label, top_n=8)
        render_dimension_comparison_bar(categorias, f"Categorias | {previous_label} x {current_label}", previous_label, current_label, height=380)

    itens = compare_dimension(previous_df, current_df, "item", previous_label, current_label, top_n=12)
    render_dimension_comparison_bar(itens, f"Itens | {previous_label} x {current_label}", previous_label, current_label, height=420)


def render_operational_comparison(
    previous: Dict[str, float],
    current: Dict[str, float],
    previous_label: str,
    current_label: str,
) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header(f"Comparativo operacional | {previous_label} x {current_label}")
    st.markdown(
        '<div class="small-muted">Comparação direta das principais dores operacionais entre os dois meses.</div>',
        unsafe_allow_html=True,
    )

    comp = build_comparison(previous, current)
    chart_df = comp.rename(columns={"Mês anterior": previous_label, "Mês atual": current_label})
    col1, col2 = st.columns(2)

    with col1:
        render_vertical_chart(
            chart_df,
            {
                "Backlog por status": "Backlog",
                "Fora SLA": "Fora SLA",
                "Tratados acima de 72h": "Acima 72h",
                "Em aberto / sem encerramento": "Sem encerr.",
            },
            "Dores em quantidade",
            "Backlog, atrasos e chamados sem encerramento.",
            previous_label,
            current_label,
            "Quantidade",
            is_percentage=False,
            height=390,
        )

    with col2:
        render_vertical_chart(
            chart_df,
            {"% SLA": "% SLA", "% 1º retorno até 1h": "% 1º retorno", "% FCR 1h": "% FCR 1h"},
            "Dores percentuais",
            "SLA, primeiro retorno e resolução em até 1 hora.",
            previous_label,
            current_label,
            "Percentual (%)",
            is_percentage=True,
            height=390,
        )

    operational_indicators = [
        "% SLA",
        "Backlog por status",
        "% 1º retorno até 1h",
        "Fora SLA",
        "Tratados acima de 72h",
        "Em aberto / sem encerramento",
        "% FCR 1h",
    ]
    operational_table = comp[comp["Indicador"].isin(operational_indicators)].copy()
    with st.expander("Ver tabela detalhada do comparativo operacional"):
        display_comparison_table(operational_table)


def render_sector_pie(current_df: pd.DataFrame) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Setores com maior demanda")
    st.markdown(
        '<div class="small-muted">Distribuição dos setores com maior volume de chamados no mês atual.</div>',
        unsafe_allow_html=True,
    )
    setores = top_table(current_df, "setor", top_n=5, include_other=True)
    render_pie_chart_from_table(setores, "Distribuição por setor", height=350)


def render_pain_points_section(current: Dict[str, float], current_label: str) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Principais dores operacionais")
    st.markdown(
        '<div class="small-muted">Cruzamento de volume com risco operacional: SLA, backlog, primeiro retorno e tempo de resolução.</div>',
        unsafe_allow_html=True,
    )
    dores = pain_points(current)
    status_counts = dores.groupby("Status").size().reset_index(name="Quantidade")

    col1, col2 = st.columns([1, 2])
    with col1:
        fig_dores = px.pie(
            status_counts,
            names="Status",
            values="Quantidade",
            title="Resumo das dores",
            hole=0.45,
            color="Status",
            color_discrete_map={"Bom": "#059669", "Crítico": "#DC2626"},
        )
        fig_dores.update_traces(textinfo="label+value+percent", textfont_size=12, marker=dict(line=dict(color="#FFFFFF", width=2)))
        fig_dores.update_layout(
            height=330,
            font=PLOT_FONT,
            title_font=dict(size=16, color="#0F172A"),
            legend_font=dict(size=10, color="#0F172A"),
            margin=dict(l=5, r=5, t=45, b=5),
            paper_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig_dores, use_container_width=True)

    with col2:
        st.dataframe(dores, use_container_width=True, hide_index=True)

    critical = dores.loc[dores["Status"] == "Crítico", "Dor / Indicador"].tolist()
    if critical:
        st.markdown(
            f"<div class='alert-box'>Análise de dores operacionais para <b>{current_label}</b>: identificamos pontos críticos em: <b>{', '.join(critical)}</b>.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='note-box'>Análise de dores operacionais para <b>{current_label}</b>: nenhum ponto crítico identificado pelos critérios atuais.</div>",
            unsafe_allow_html=True,
        )


def render_top_impactadores(current_df: pd.DataFrame) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Top impactadores do mês atual")
    st.markdown(
        '<div class="small-muted">Clientes, responsáveis e itens em barras para facilitar leitura. Setores e categorias em pizza por terem menos grupos.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        clientes = top_table(current_df, "empresa", top_n=10, include_other=False)
        render_horizontal_bar_from_table(clientes, "Clientes | Top 10", height=340)
    with col2:
        setores = top_table(current_df, "setor", top_n=5, include_other=True)
        render_pie_chart_from_table(setores, "Setores", height=340)

    col3, col4 = st.columns(2)
    with col3:
        responsaveis = top_table(current_df, "responsavel", top_n=10, include_other=False)
        render_horizontal_bar_from_table(responsaveis, "Responsáveis | Top 10", height=340)
    with col4:
        categorias = top_table(current_df, "categoria", top_n=5, include_other=True)
        render_pie_chart_from_table(categorias, "Categorias", height=340)

    itens = top_table(current_df, "item", top_n=10, include_other=False)
    render_horizontal_bar_from_table(itens, "Itens | Top 10", height=360)


def render_current_sections(
    current_df: pd.DataFrame,
    current: Dict[str, float],
    current_label: str,
    show_current_overview: bool,
) -> None:
    if show_current_overview:
        render_current_overview(current, current_label)

    render_sector_pie(current_df)
    # Seção removida: "Principais dores operacionais"
    render_top_impactadores(current_df)



MONTH_ALIASES = {
    "janeiro": 1,
    "jan": 1,
    "fevereiro": 2,
    "fev": 2,
    "março": 3,
    "marco": 3,
    "mar": 3,
    "abril": 4,
    "abr": 4,
    "maio": 5,
    "mai": 5,
    "junho": 6,
    "jun": 6,
    "julho": 7,
    "jul": 7,
    "agosto": 8,
    "ago": 8,
    "setembro": 9,
    "set": 9,
    "outubro": 10,
    "out": 10,
    "novembro": 11,
    "nov": 11,
    "dezembro": 12,
    "dez": 12,
}

MONTH_NAMES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


def detect_month_from_filename(filename: str, fallback_order: int) -> tuple[str, int]:
    name = filename.lower()
    name = (
        name.replace("_", " ")
        .replace("-", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(".", " ")
    )
    name = " ".join(name.split())

    for token, month_number in MONTH_ALIASES.items():
        if token in name:
            return MONTH_NAMES[month_number], month_number

    return f"Relatório {fallback_order}", 100 + fallback_order


def metrics_to_summary_row(
    label: str,
    order: int,
    metrics: Dict[str, float],
    filename: str,
) -> Dict[str, Any]:
    return {
        "Mês": label,
        "Ordem": order,
        "Arquivo": filename,
        "Total de chamados": metrics.get("Total de chamados", 0),
        "Dentro SLA": metrics.get("Dentro SLA", 0),
        "Fora SLA": metrics.get("Fora SLA", 0),
        "% SLA": metrics.get("% SLA", 0),
        "Tratados até 72h": metrics.get("Tratados até 72h", 0),
        "Tratados acima de 72h": metrics.get("Tratados acima de 72h", 0),
        "Em aberto / sem encerramento": metrics.get("Em aberto / sem encerramento", 0),
        "Backlog por status": metrics.get("Backlog por status", 0),
        "Empresas": metrics.get("Empresas", 0),
        "FCR tratado": metrics.get("FCR tratado", 0),
        "First Call Resolution até 1h": metrics.get("First Call Resolution até 1h", 0),
        "Resolvidos acima de 1h": metrics.get("Resolvidos acima de 1h", 0),
        "% FCR 1h": metrics.get("% FCR 1h", 0),
        "% 1º retorno até 1h": metrics.get("% 1º retorno até 1h", 0),
    }


def build_historical_dataset(uploaded_files: list[Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary_rows = []
    base_parts = []

    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        label, order = detect_month_from_filename(uploaded_file.name, idx)
        df = read_excel_smart(uploaded_file)

        if df.empty:
            continue

        metrics = calculate_metrics(df)
        if not metrics:
            continue

        df = df.copy()
        df["Mês"] = label
        df["Ordem mês"] = order
        df["Arquivo origem"] = uploaded_file.name

        summary_rows.append(metrics_to_summary_row(label, order, metrics, uploaded_file.name))
        base_parts.append(df)

    if not summary_rows:
        return pd.DataFrame(), pd.DataFrame()

    summary_df = pd.DataFrame(summary_rows).sort_values("Ordem").reset_index(drop=True)
    combined_df = pd.concat(base_parts, ignore_index=True) if base_parts else pd.DataFrame()

    return summary_df, combined_df


def display_historical_kpis(summary_df: pd.DataFrame) -> None:
    total_chamados = int(summary_df["Total de chamados"].sum())
    qtd_meses = int(summary_df["Mês"].nunique())
    media_mensal = total_chamados / qtd_meses if qtd_meses else 0
    sla_medio = float(summary_df["% SLA"].mean()) if not summary_df.empty else 0

    melhor_idx = summary_df["% SLA"].idxmax()
    pior_idx = summary_df["% SLA"].idxmin()

    melhor_mes = summary_df.loc[melhor_idx, "Mês"]
    melhor_sla = summary_df.loc[melhor_idx, "% SLA"]

    pior_mes = summary_df.loc[pior_idx, "Mês"]
    pior_sla = summary_df.loc[pior_idx, "% SLA"]

    cols = st.columns(5)

    with cols[0]:
        kpi_card("Total no período", format_int(total_chamados), f"{qtd_meses} relatórios", "neutral")

    with cols[1]:
        kpi_card("Média mensal", format_int(media_mensal), "Chamados por mês", "neutral")

    with cols[2]:
        status = "good" if sla_medio >= 80 else "bad"
        kpi_card("SLA médio", format_pct(sla_medio), "Meta: ≥ 80%", status)

    with cols[3]:
        kpi_card("Melhor SLA", format_pct(melhor_sla), str(melhor_mes), "good")

    with cols[4]:
        status = "good" if pior_sla >= 80 else "bad"
        kpi_card("Pior SLA", format_pct(pior_sla), str(pior_mes), status)


def render_history_line_chart(
    summary_df: pd.DataFrame,
    y_column: str,
    title: str,
    y_title: str,
    is_percentage: bool = False,
    meta: Optional[float] = None,
    height: int = 370,
) -> None:
    fig = px.line(
        summary_df,
        x="Mês",
        y=y_column,
        markers=True,
        text=y_column,
        title=title,
    )

    if is_percentage:
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="top center")
        y_max = max(float(summary_df[y_column].max()), meta or 0, 10)
        fig.update_layout(yaxis_range=[0, y_max + 15])
    else:
        fig.update_traces(texttemplate="%{text:.0f}", textposition="top center")
        y_max = max(float(summary_df[y_column].max()), 10)
        fig.update_layout(yaxis_range=[0, y_max * 1.18])

    if meta is not None:
        fig.add_hline(
            y=meta,
            line_dash="dash",
            line_color="#DC2626",
            annotation_text=f"Meta {format_pct(meta) if is_percentage else format_int(meta)}",
            annotation_position="top left",
        )

    fig.update_layout(
        height=height,
        xaxis_title="",
        yaxis_title=y_title,
        font=PLOT_FONT,
        margin=dict(l=10, r=20, t=55, b=40),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )

    fig.update_xaxes(tickfont=dict(size=11, color="#0F172A"))
    fig.update_yaxes(tickfont=dict(size=11, color="#0F172A"), gridcolor="#E5E7EB")

    st.plotly_chart(fig, use_container_width=True)


def render_history_bar_chart(
    summary_df: pd.DataFrame,
    y_column: str,
    title: str,
    y_title: str,
    height: int = 350,
) -> None:
    fig = px.bar(
        summary_df,
        x="Mês",
        y=y_column,
        text=y_column,
        title=title,
        color_discrete_sequence=["#2563EB"],
    )

    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")

    y_max = max(float(summary_df[y_column].max()), 10)
    fig.update_layout(
        height=height,
        xaxis_title="",
        yaxis_title=y_title,
        font=PLOT_FONT,
        yaxis_range=[0, y_max * 1.18],
        margin=dict(l=10, r=20, t=55, b=40),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        showlegend=False,
    )

    fig.update_xaxes(tickfont=dict(size=11, color="#0F172A"))
    fig.update_yaxes(tickfont=dict(size=11, color="#0F172A"), gridcolor="#E5E7EB")

    st.plotly_chart(fig, use_container_width=True)


def render_historical_evolution(summary_df: pd.DataFrame) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Evolução mensal")
    st.markdown(
        '<div class="small-muted">Visão histórica dos principais indicadores mês a mês.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        render_history_bar_chart(
            summary_df,
            "Total de chamados",
            "Volume mensal de chamados",
            "Quantidade",
            height=350,
        )

    with col2:
        render_history_line_chart(
            summary_df,
            "% SLA",
            "Evolução do SLA mensal",
            "Percentual (%)",
            is_percentage=True,
            meta=80,
            height=350,
        )

    col3, col4 = st.columns(2)

    with col3:
        render_history_line_chart(
            summary_df,
            "% 1º retorno até 1h",
            "Evolução do 1º retorno até 1h",
            "Percentual (%)",
            is_percentage=True,
            meta=70,
            height=350,
        )

    with col4:
        render_history_bar_chart(
            summary_df,
            "Backlog por status",
            "Backlog por mês",
            "Quantidade",
            height=350,
        )

    col5, col6 = st.columns(2)

    with col5:
        render_history_bar_chart(
            summary_df,
            "Tratados acima de 72h",
            "Chamados acima de 72h por mês",
            "Quantidade",
            height=350,
        )

    with col6:
        render_history_line_chart(
            summary_df,
            "% FCR 1h",
            "Evolução do FCR até 1h",
            "Percentual (%)",
            is_percentage=True,
            height=350,
        )


def build_month_over_month(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Base formatada para a tabela detalhada de variação mês a mês."""
    df = summary_df.sort_values("Ordem").copy()

    compare_cols = [
        "Total de chamados",
        "% SLA",
        "Dentro SLA",
        "Fora SLA",
        "% 1º retorno até 1h",
        "% FCR 1h",
        "Backlog por status",
        "Tratados acima de 72h",
        "Em aberto / sem encerramento",
    ]

    rows = []

    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        for col in compare_cols:
            previous_value = float(prev[col])
            current_value = float(curr[col])
            diff = current_value - previous_value
            is_pct = col.startswith("%")
            variation = pct(diff, previous_value) if (not is_pct and previous_value != 0) else None
            direction_class = delta_direction_class(col, diff)

            if direction_class == "positive":
                reading = "✅ Melhorou"
            elif direction_class == "negative":
                reading = "⚠️ Piorou"
            else:
                reading = "• Neutro"

            rows.append(
                {
                    "Comparação": f"{prev['Mês']} → {curr['Mês']}",
                    "Indicador": col,
                    "Anterior": format_pct(previous_value) if is_pct else format_int(previous_value),
                    "Atual": format_pct(current_value) if is_pct else format_int(current_value),
                    "Diferença": format_pp(diff) if is_pct else f"{int(diff):+d}",
                    "Variação": "-" if is_pct or variation is None else format_pct(variation),
                    "Leitura": reading,
                    "Classe": direction_class,
                }
            )

    return pd.DataFrame(rows)


def render_mom_card(indicator: str, previous_row: pd.Series, current_row: pd.Series) -> None:
    previous_value = float(previous_row[indicator])
    current_value = float(current_row[indicator])
    diff = current_value - previous_value
    card_class = delta_direction_class(indicator, diff)
    delta_label = delta_text(indicator, current_value, previous_value, str(previous_row["Mês"]))

    st.markdown(
        f'<div class="evo-card {card_class}">'
        f'<div class="evo-label">{indicator}</div>'
        f'<div class="evo-value">{format_metric(indicator, current_value)}</div>'
        f'<div class="evo-delta {card_class}">{delta_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_month_over_month(summary_df: pd.DataFrame) -> None:
    if len(summary_df) < 2:
        return

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Comparativo mês a mês")
    st.markdown(
        '<div class="small-muted">Resumo visual da variação de cada mês em relação ao mês anterior. A tabela completa fica separada para não poluir a leitura.</div>',
        unsafe_allow_html=True,
    )

    ordered = summary_df.sort_values("Ordem").reset_index(drop=True)
    mom_df = build_month_over_month(ordered)

    tab_resumo, tab_tabela = st.tabs(["Resumo visual", "Tabela completa"])

    with tab_resumo:
        card_indicators = [
            "Total de chamados",
            "% SLA",
            "% 1º retorno até 1h",
            "Backlog por status",
            "Tratados acima de 72h",
        ]

        for i in range(1, len(ordered)):
            prev = ordered.iloc[i - 1]
            curr = ordered.iloc[i]
            comparison_label = f"{prev['Mês']} → {curr['Mês']}"

            st.markdown(f"### {comparison_label}")
            cols = st.columns(5)
            for col, indicator in zip(cols, card_indicators):
                with col:
                    render_mom_card(indicator, prev, curr)

            comparison_rows = mom_df[mom_df["Comparação"] == comparison_label]
            worse = comparison_rows.loc[comparison_rows["Classe"] == "negative", "Indicador"].tolist()
            better = comparison_rows.loc[comparison_rows["Classe"] == "positive", "Indicador"].tolist()

            if worse:
                st.markdown(
                    f"<div class='alert-box'><b>Atenção em {comparison_label}:</b> piora em <b>{', '.join(worse)}</b>.</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='note-box'><b>{comparison_label}:</b> nenhum indicador crítico piorou pelos critérios atuais.</div>",
                    unsafe_allow_html=True,
                )

            if better:
                st.markdown(
                    f"<div class='note-box'><b>Melhoras observadas:</b> {', '.join(better)}.</div>",
                    unsafe_allow_html=True,
                )

    with tab_tabela:
        table_df = mom_df.drop(columns=["Classe"])
        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                "Comparação": st.column_config.TextColumn("Comparação", width="small"),
                "Indicador": st.column_config.TextColumn("Indicador", width="medium"),
                "Anterior": st.column_config.TextColumn("Anterior", width="small"),
                "Atual": st.column_config.TextColumn("Atual", width="small"),
                "Diferença": st.column_config.TextColumn("Diferença", width="small"),
                "Variação": st.column_config.TextColumn("Variação", width="small"),
                "Leitura": st.column_config.TextColumn("Leitura", width="small"),
            },
        )

        st.markdown(
            "<div class='small-muted'>Use esta tabela apenas para conferência detalhada. Para apresentação executiva, o resumo visual acima é mais claro.</div>",
            unsafe_allow_html=True,
        )


def render_historical_rankings(combined_df: pd.DataFrame) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Ranking acumulado do período")
    st.markdown(
        '<div class="small-muted">Principais clientes, setores, responsáveis, categorias e itens considerando todos os relatórios carregados.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        clientes = top_table(combined_df, "empresa", top_n=10, include_other=False)
        render_horizontal_bar_from_table(clientes, "Clientes | Top 10 do período", height=340)

    with col2:
        setores = top_table(combined_df, "setor", top_n=5, include_other=True)
        render_pie_chart_from_table(setores, "Setores no período", height=340)

    col3, col4 = st.columns(2)

    with col3:
        responsaveis = top_table(combined_df, "responsavel", top_n=10, include_other=False)
        render_horizontal_bar_from_table(responsaveis, "Responsáveis | Top 10 do período", height=340)

    with col4:
        categorias = top_table(combined_df, "categoria", top_n=5, include_other=True)
        render_pie_chart_from_table(categorias, "Categorias no período", height=340)

    itens = top_table(combined_df, "item", top_n=10, include_other=False)
    render_horizontal_bar_from_table(itens, "Itens | Top 10 do período", height=360)


def render_executive_history_reading(summary_df: pd.DataFrame) -> None:
    if summary_df.empty:
        return

    first = summary_df.iloc[0]
    last = summary_df.iloc[-1]

    diff_volume = float(last["Total de chamados"]) - float(first["Total de chamados"])
    diff_sla = float(last["% SLA"]) - float(first["% SLA"])
    diff_retorno = float(last["% 1º retorno até 1h"]) - float(first["% 1º retorno até 1h"])
    diff_backlog = float(last["Backlog por status"]) - float(first["Backlog por status"])

    melhor_mes = summary_df.loc[summary_df["% SLA"].idxmax(), "Mês"]
    pior_mes = summary_df.loc[summary_df["% SLA"].idxmin(), "Mês"]

    st.markdown(
        f"""
        <div class='note-box'>
        <b>Leitura executiva do período:</b> do primeiro ao último relatório carregado,
        o volume variou <b>{int(diff_volume):+d} chamados</b>.
        O SLA mudou <b>{format_pp(diff_sla)}</b>, o primeiro retorno até 1h mudou
        <b>{format_pp(diff_retorno)}</b> e o backlog variou <b>{int(diff_backlog):+d}</b>.
        O melhor mês de SLA foi <b>{melhor_mes}</b> e o pior mês foi <b>{pior_mes}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_historical_mode() -> None:
    with st.sidebar:
        st.header("Histórico")
        st.caption("Envie vários relatórios mensais. O nome do arquivo deve conter o mês, exemplo: janeiro, fevereiro, março.")
        historical_uploads = st.file_uploader(
            "Relatórios mensais",
            type=["xls", "xlsx"],
            accept_multiple_files=True,
            key="historical_uploads",
        )

    if not historical_uploads:
        st.info("Envie dois ou mais relatórios mensais para iniciar o estudo histórico.")
        st.stop()

    summary_df, combined_df = build_historical_dataset(historical_uploads)

    if summary_df.empty:
        st.error("Não consegui ler dados válidos nos relatórios enviados.")
        st.stop()

    display_historical_kpis(summary_df)
    render_executive_history_reading(summary_df)
    render_historical_evolution(summary_df)
    render_month_over_month(summary_df)
    render_historical_rankings(combined_df)

    with st.expander("Ver resumo mensal consolidado"):
        display_cols = [
            "Mês",
            "Arquivo",
            "Total de chamados",
            "Dentro SLA",
            "Fora SLA",
            "% SLA",
            "% 1º retorno até 1h",
            "% FCR 1h",
            "Backlog por status",
            "Tratados acima de 72h",
            "Em aberto / sem encerramento",
            "Empresas",
        ]

        formatted = summary_df[display_cols].copy()
        for col in ["% SLA", "% 1º retorno até 1h", "% FCR 1h"]:
            formatted[col] = formatted[col].map(format_pct)

        for col in [
            "Total de chamados",
            "Dentro SLA",
            "Fora SLA",
            "Backlog por status",
            "Tratados acima de 72h",
            "Em aberto / sem encerramento",
            "Empresas",
        ]:
            formatted[col] = formatted[col].map(format_int)

        st.dataframe(formatted, use_container_width=True, hide_index=True)


def render_two_month_mode() -> None:
    with st.sidebar:
        st.header("Upload das bases")
        st.caption("1º passo: carregue o mês atual, por exemplo Maio. O dashboard já aparece.")
        current_label = st.text_input("Nome do mês atual", value="Maio")
        current_upload = st.file_uploader("1) Arquivo do mês atual", type=["xls", "xlsx"], key="current")

        st.divider()

        st.caption("2º passo: carregue o mês anterior, por exemplo Abril. A comparação será liberada.")
        previous_label = st.text_input("Nome do mês anterior", value="Abril")
        previous_upload = st.file_uploader("2) Arquivo do mês anterior", type=["xls", "xlsx"], key="previous")

        st.divider()
        st.caption("Metas usadas nos cards: SLA ≥ 80% | 1º retorno até 1h ≥ 70%")

    if current_upload is None:
        st.info("Carregue primeiro o arquivo do mês atual, por exemplo o consolidado de Maio.")
        st.stop()

    current_df = read_excel_smart(current_upload)
    if current_df.empty:
        st.error("Não consegui ler o arquivo do mês atual. Confirme se é um Excel .xls ou .xlsx exportado do sistema.")
        st.stop()

    current = calculate_metrics(current_df)
    if not current:
        st.error("O arquivo foi lido, mas não encontrei linhas válidas de chamados.")
        st.stop()

    previous_df = pd.DataFrame()
    previous: Optional[Dict[str, float]] = None

    if previous_upload is not None:
        previous_df = read_excel_smart(previous_upload)
        if previous_df.empty:
            st.warning("O arquivo do mês anterior foi carregado, mas não consegui encontrar dados válidos.")
        else:
            previous = calculate_metrics(previous_df)

    render_kpis(current, previous, current_label, previous_label)

    if previous is None:
        st.markdown(
            f"<div class='note-box'><b>{current_label} carregado com sucesso.</b> O dashboard abaixo mostra as informações do mês atual. Para ver a diferença nos KPIs, nos cards e nos gráficos, envie também o arquivo de {previous_label} no menu lateral.</div>",
            unsafe_allow_html=True,
        )
        render_current_sections(
            current_df=current_df,
            current=current,
            current_label=current_label,
            show_current_overview=True,
        )

    else:
        st.markdown(
            f"<div class='note-box'><b>{current_label} e {previous_label} carregados com sucesso.</b> O dashboard agora está em modo comparativo: {previous_label} x {current_label}.</div>",
            unsafe_allow_html=True,
        )

        render_evolution_cards(previous, current, previous_label, current_label)
        comp = render_comparison_charts(previous, current, previous_label, current_label)
        render_comparison_table_and_reading(comp, previous_label, current_label)

        render_dimension_comparison(
            previous_df=previous_df,
            current_df=current_df,
            previous_label=previous_label,
            current_label=current_label,
        )

        render_operational_comparison(
            previous=previous,
            current=current,
            previous_label=previous_label,
            current_label=current_label,
        )

    with st.expander("Ver prévia da base carregada"):
        st.write(f"**{current_label}:** {current_df.shape[0]} linhas e {current_df.shape[1]} colunas")
        st.dataframe(current_df.head(20), use_container_width=True)

        if previous is not None:
            st.write(f"**{previous_label}:** {previous_df.shape[0]} linhas e {previous_df.shape[1]} colunas")
            st.dataframe(previous_df.head(20), use_container_width=True)


def main() -> None:
    st.markdown(
        '<div class="main-title">Dashboard de Chamados | SLA, Backlog e Operação</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sub-title">Escolha entre comparação de 2 meses ou estudo histórico com vários relatórios.</div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        analysis_mode = st.radio(
            "Tipo de análise",
            ["Comparação entre 2 meses", "Histórico com vários meses"],
        )

        st.divider()

    if analysis_mode == "Comparação entre 2 meses":
        render_two_month_mode()
    else:
        render_historical_mode()


if __name__ == "__main__":
    main()
