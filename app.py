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
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
.main-title {font-size: 2.1rem; font-weight: 800; margin-bottom: 0.2rem; color: #111827;}
.sub-title {font-size: 0.98rem; color: #6B7280; margin-bottom: 1.2rem;}
.kpi-card {
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
    border-left: 6px solid #64748B;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.08);
    padding: 18px 16px 16px 16px;
    min-height: 118px;
}
.kpi-card.good {background: #ECFDF5; border-color: #A7F3D0; border-left-color: #10B981;}
.kpi-card.bad {background: #FEF2F2; border-color: #FECACA; border-left-color: #EF4444;}
.kpi-label {font-size: 0.76rem; color: #64748B; font-weight: 800; text-transform: uppercase; letter-spacing: .055rem; text-align: center;}
.kpi-value {font-size: 1.95rem; color: #020617; font-weight: 900; line-height: 1.2; text-align: center; margin-top: 8px;}
.kpi-help {font-size: 0.80rem; color: #475569; text-align: center; margin-top: 8px;}
.kpi-help.good-text {color: #059669; font-weight: 700;}
.kpi-help.bad-text {color: #DC2626; font-weight: 700;}
.section-divider {border: 0; border-top: 1px solid #CBD5E1; margin: 2.0rem 0 1.7rem 0;}
.note-box {
    border-left: 5px solid #2563EB;
    background: #F8FAFC;
    border-radius: 9px;
    padding: 15px 18px;
    margin-top: 18px;
    color: #0F172A;
}
.alert-box {
    border-left: 5px solid #EF4444;
    background: #FEF2F2;
    border-radius: 9px;
    padding: 15px 18px;
    margin-top: 18px;
    color: #0F172A;
}
.small-muted {color: #6B7280; font-size: 0.9rem;}
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

    empresas_unicas = empresa.dropna().astype(str).str.strip().replace("", pd.NA).dropna().nunique()

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


def format_metric(indicator: str, value: float) -> str:
    return format_pct(value) if indicator.startswith("%") else format_int(value)


def format_pp(value: float) -> str:
    return f"{value:+.1f}".replace(".", ",") + " p.p."


def kpi_card(label: str, value: str, help_text: str, status: str = "neutral") -> None:
    css_class = "good" if status == "good" else "bad" if status == "bad" else ""
    help_class = "good-text" if status == "good" else "bad-text" if status == "bad" else ""
    st.markdown(
        f"""
        <div class="kpi-card {css_class}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-help {help_class}">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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


def top_table(df: pd.DataFrame, key: str, top_n: int = 5) -> pd.DataFrame:
    col = find_col(df, key)
    if col is None:
        return pd.DataFrame(columns=["Nome", "Quantidade", "% do total"])
    values = df[col].dropna().astype(str).str.strip()
    values = values[values != ""]
    counts = values.value_counts().head(top_n)
    total = len(df) if len(df) else 1
    return pd.DataFrame(
        {
            "Nome": counts.index,
            "Quantidade": counts.values,
            "% do total": [format_pct(pct(v, total), 1) for v in counts.values],
        }
    )


def display_rank_block(title: str, table: pd.DataFrame) -> None:
    st.markdown(f"**{title}**")
    if table.empty:
        st.info("Coluna não encontrada na base.")
    else:
        st.dataframe(table, use_container_width=True, hide_index=True, height=230)


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


def render_kpis(current: Dict[str, float]) -> None:
    kpi_cols = st.columns(5)
    with kpi_cols[0]:
        kpi_card("Total de chamados", format_int(current["Total de chamados"]), "Visão do mês")
    with kpi_cols[1]:
        sla_status = "good" if current["% SLA"] >= 80 else "bad"
        kpi_card("% Dentro do SLA", format_pct(current["% SLA"]), "Meta: ≥ 80%", sla_status)
    with kpi_cols[2]:
        retorno_status = "good" if current["% 1º retorno até 1h"] >= 70 else "bad"
        kpi_card("% 1º retorno até 1h", format_pct(current["% 1º retorno até 1h"]), "Meta: ≥ 70%", retorno_status)
    with kpi_cols[3]:
        status = "bad" if current["Backlog por status"] > 0 else "good"
        kpi_card("Backlog por status", format_int(current["Backlog por status"]), "Sem encerr. / status", status)
    with kpi_cols[4]:
        status = "bad" if current["Tratados acima de 72h"] > 0 else "good"
        kpi_card("Tratados acima de 72h", format_int(current["Tratados acima de 72h"]), "Encerrados > 72h", status)


def render_comparison(previous: Dict[str, float], current: Dict[str, float], previous_label: str, current_label: str) -> None:
    comp = build_comparison(previous, current)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Comparação entre mês anterior e mês atual")
    st.markdown(
        f'<div class="small-muted">Ordem cronológica: primeiro {previous_label}, depois {current_label}. A comparação aparece somente depois que os dois arquivos são carregados.</div>',
        unsafe_allow_html=True,
    )

    chart_df = comp.rename(columns={"Mês anterior": previous_label, "Mês atual": current_label})
    for chart_type, title in [
        ("Quantidade", "Comparativo em barras | Volumes e produtividade"),
        ("Percentual", "Comparativo em barras | Indicadores percentuais"),
    ]:
        filtered = chart_df[chart_df["Tipo"] == chart_type].copy()
        long_df = filtered.melt(
            id_vars="Indicador",
            value_vars=[previous_label, current_label],
            var_name="Mês",
            value_name="Valor",
        )
        fig = px.bar(
            long_df,
            y="Indicador",
            x="Valor",
            color="Mês",
            barmode="group",
            orientation="h",
            text="Valor",
            title=title,
        )
        fig.update_traces(texttemplate="%{x:.1f}" if chart_type == "Percentual" else "%{x:.0f}", textposition="outside")
        fig.update_layout(
            height=max(430, 40 * filtered.shape[0]),
            xaxis_title="Percentual (%)" if chart_type == "Percentual" else "Quantidade",
            yaxis_title="",
            legend_title="",
            margin=dict(l=20, r=60, t=60, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Comparativo geral")
    display_comparison_table(comp)

    total_row = comp.loc[comp["Indicador"] == "Total de chamados"].iloc[0]
    sla_row = comp.loc[comp["Indicador"] == "% SLA"].iloc[0]
    retorno_row = comp.loc[comp["Indicador"] == "% 1º retorno até 1h"].iloc[0]
    st.markdown(
        f"""
        <div class='note-box'>
        <b>Leitura da evolução:</b> de {previous_label} para {current_label}, o volume variou
        <b>{int(total_row['Diferença']):+d} chamados</b> ({format_pct(total_row['Variação %'])}).
        O SLA mudou <b>{format_pp(sla_row['Diferença'])}</b> e o primeiro retorno até 1h mudou
        <b>{format_pp(retorno_row['Diferença'])}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_current_sections(current_df: pd.DataFrame, current: Dict[str, float], current_label: str) -> None:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header(f"Comparativo geral do mês atual | {current_label}")
    st.dataframe(current_overview_table(current), use_container_width=True, hide_index=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Setores com maior demanda")
    st.markdown('<div class="small-muted">Ranking de setores com maior volume de chamados no mês atual.</div>', unsafe_allow_html=True)
    setores = top_table(current_df, "setor", 10)
    if not setores.empty:
        fig_setores = px.bar(setores, x="Quantidade", y="Nome", orientation="h", text="Quantidade", title="Volume por setor")
        fig_setores.update_traces(textposition="outside")
        fig_setores.update_layout(height=420, yaxis_title="", xaxis_title="Quantidade", margin=dict(l=20, r=60, t=60, b=20))
        st.plotly_chart(fig_setores, use_container_width=True)
    st.dataframe(setores, use_container_width=True, hide_index=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Principais dores operacionais")
    st.markdown(
        '<div class="small-muted">Cruzamento de volume com risco operacional: SLA, backlog, primeiro retorno e tempo de resolução.</div>',
        unsafe_allow_html=True,
    )
    dores = pain_points(current)
    st.dataframe(dores, use_container_width=True, hide_index=True)
    critical = dores.loc[dores["Status"] == "Crítico", "Dor / Indicador"].tolist()
    if critical:
        st.markdown(
            f"<div class='alert-box'>Análise de dores operacionais para <b>{current_label}</b>: identificamos pontos críticos em: <b>{', '.join(critical)}</b>.</div>",
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Top impactadores do mês atual")
    st.markdown(
        '<div class="small-muted">Principais concentrações de chamados por dimensão: clientes, setores, responsáveis, categorias e itens.</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        display_rank_block("Clientes", top_table(current_df, "empresa", 5))
    with c2:
        display_rank_block("Setores", top_table(current_df, "setor", 5))
    with c3:
        display_rank_block("Responsáveis", top_table(current_df, "responsavel", 5))
    with c4:
        display_rank_block("Categorias", top_table(current_df, "categoria", 5))
    with c5:
        display_rank_block("Itens", top_table(current_df, "item", 5))


def main() -> None:
    st.markdown('<div class="main-title">Dashboard de Chamados | SLA, Backlog e Operação</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Fluxo progressivo: primeiro carregue o mês atual. Depois carregue o mês anterior para comparar.</div>',
        unsafe_allow_html=True,
    )

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

    render_kpis(current)

    st.markdown(
        f"<div class='note-box'><b>{current_label} carregado com sucesso.</b> O dashboard abaixo mostra as informações do mês atual. Para ver a diferença, envie também o arquivo de {previous_label} no menu lateral.</div>",
        unsafe_allow_html=True,
    )

    if previous_upload is not None:
        previous_df = read_excel_smart(previous_upload)
        if previous_df.empty:
            st.warning("O arquivo do mês anterior foi carregado, mas não consegui encontrar dados válidos. A comparação foi ignorada.")
        else:
            previous = calculate_metrics(previous_df)
            render_comparison(previous, current, previous_label, current_label)

    render_current_sections(current_df, current, current_label)

    with st.expander("Ver prévia da base carregada"):
        st.write(f"**{current_label}:** {current_df.shape[0]} linhas e {current_df.shape[1]} colunas")
        st.dataframe(current_df.head(20), use_container_width=True)
        if previous_upload is not None:
            previous_df = read_excel_smart(previous_upload)
            st.write(f"**{previous_label}:** {previous_df.shape[0]} linhas e {previous_df.shape[1]} colunas")
            st.dataframe(previous_df.head(20), use_container_width=True)


if __name__ == "__main__":
    main()
