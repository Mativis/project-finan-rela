import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Financas do Casal", page_icon="💰", layout="wide", initial_sidebar_state="expanded")

API_URL = 'https://script.google.com/macros/s/AKfycbwHV5_tLRl4F52tJBT3ttw605fwLBfgLa5823DrNqQjDnfbRs90ZOEighmhlHTo-H1Z/exec'

# ═══════════════════════════════════════════════════════════════════════════════
# CSS COMPLETO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg:        #f1f5f9;
    --surface:   #ffffff;
    --surface2:  #f8fafc;
    --border:    #e2e8f0;
    --text:      #0f172a;
    --text2:     #475569;
    --text3:     #94a3b8;
    --accent:    #475569;
    --accent2:   #64748b;
    --accent-bg: #f1f5f9;
    --green:     #22c55e;
    --green-bg:  #f0fdf4;
    --green-br:  #bbf7d0;
    --red:       #ef4444;
    --red-bg:    #fef2f2;
    --red-br:    #fecaca;
    --orange:    #f97316;
    --orange-bg: #fff7ed;
    --orange-br: #fed7aa;
    --blue:      #64748b;
    --blue-bg:   #f1f5f9;
    --blue-br:   #cbd5e1;
    --radius:    12px;
    --radius-lg: 16px;
    --shadow:    0 1px 3px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.12);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

section[data-testid="stSidebar"] {
    background: linear-gradient(195deg, #0f172a 0%, #1e293b 100%) !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] hr { border-color: #334155 !important; }

.sb-brand { text-align:center; padding:1.5rem 0 1rem; }
.sb-brand h1 { color:#f1f5f9 !important; font-size:1.15rem !important; font-weight:800 !important; letter-spacing:-0.03em; margin:0 !important; }
.sb-brand span { color:#94a3b8 !important; font-size:0.7rem; font-weight:500; letter-spacing:0.06em; text-transform:uppercase; }
.sb-brand hr { border-color:#334155 !important; margin-top:1rem !important; }

section[data-testid="stSidebar"] .stRadio > div { gap:2px !important; }
section[data-testid="stSidebar"] [data-baseweb="radio"] {
    background: transparent !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"]:hover {
    background: rgba(71,85,105,0.08) !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"] label {
    padding: 0.55rem 0.85rem !important;
    font-size: 0.85rem !important;
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"]:hover label {
    color: #e2e8f0 !important;
}

.page-header { margin-bottom:2rem; }
.page-header h1 { font-size:1.75rem !important; font-weight:800 !important; letter-spacing:-0.03em; color:#0f172a !important; margin:0 !important; }
.page-header p { color:#64748b !important; font-size:0.9rem; margin:0.35rem 0 0 0; }

.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow);
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
    position: relative;
    overflow: hidden;
}
.stat-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }
.stat-card .label { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:var(--text3); margin-bottom:0.5rem; }
.stat-card .value { font-size:1.75rem; font-weight:800; color:var(--text); letter-spacing:-0.02em; }
.stat-card .badge { font-size:0.7rem; font-weight:600; padding:0.2rem 0.6rem; border-radius:100px; display:inline-flex; align-items:center; gap:0.25rem; margin-top:0.5rem; }
.stat-card .badge.green { background:var(--green-bg); color:var(--green); border:1px solid var(--green-br); }
.stat-card .badge.red   { background:var(--red-bg);   color:var(--red);   border:1px solid var(--red-br); }
.stat-card .badge.blue  { background:var(--accent-bg);   color:var(--accent);  border:1px solid #cbd5e1; }
.stat-card .stripe { position:absolute; top:0; left:0; width:100%; height:3px; }
.stat-card .stripe.green { background: linear-gradient(90deg, #22c55e, #4ade80); }
.stat-card .stripe.red   { background: linear-gradient(90deg, #ef4444, #f87171); }
.stat-card .stripe.blue  { background: linear-gradient(90deg, #475569, #64748b); }

.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}
.panel-title {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text3);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-title::before {
    content: '';
    width: 4px; height: 14px;
    background: var(--accent);
    border-radius: 2px;
    flex-shrink: 0;
}

.chip { display:inline-flex; align-items:center; gap:0.35rem; padding:0.4rem 0.75rem; border-radius:100px; font-size:0.75rem; font-weight:600; }
.chip.receita { background:var(--green-bg); color:var(--green); border:1px solid var(--green-br); }
.chip.despesa { background:var(--red-bg);   color:var(--red);   border:1px solid var(--red-br); }

.goal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--shadow);
    transition: all 0.2s;
}
.goal-card:hover { box-shadow: var(--shadow-md); }
.goal-card .goal-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; }
.goal-card .goal-name { font-weight:700; color:var(--text); font-size:0.95rem; }
.goal-card .goal-pct { font-weight:800; font-size:0.9rem; padding:0.2rem 0.6rem; border-radius:100px; }
.goal-card .goal-pct.done { background:var(--green-bg); color:var(--green); }
.goal-card .goal-pct.wip  { background:var(--accent-bg); color:var(--accent); }
.goal-card .goal-values { font-size:0.8rem; color:var(--text2); }
.goal-card .goal-due { font-size:0.7rem; color:var(--text3); margin-top:0.35rem; }

.empty-state { text-align:center; padding:3rem 1rem; color:var(--text3); }
.empty-state .icon { font-size:3rem; margin-bottom:1rem; opacity:0.5; }
.empty-state p { font-size:0.9rem; }

.divider { border:none; border-top:1px solid var(--border); margin:1rem 0; }

/* ── Streamlit overrides ── */
.stMetric {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.stMetric label { display:none !important; }
.stMetric [data-testid="stMetricValue"] { font-size:1.6rem !important; font-weight:800 !important; color:#0f172a !important; }
.stMetric [data-testid="stMetricDelta"] { font-size:0.75rem !important; font-weight:600 !important; }

.stButton > div > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.2s !important;
}
.stButton > div > button[kind="primary"],
.stButton > div > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #475569, #64748b) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 2px 8px rgba(71,85,105,0.3) !important;
}
.stButton > div > button[kind="primary"]:hover {
    box-shadow: 0 4px 16px rgba(71,85,105,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > div > button[kind="secondary"],
.stButton > div > button[data-testid="stBaseButton-secondary"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text2) !important;
}
.stButton > div > button[kind="secondary"]:hover {
    background: #f1f5f9 !important;
    border-color: #cbd5e1 !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface2) !important;
    font-size: 0.875rem !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(71,85,105,0.1) !important;
    background: var(--surface) !important;
}

div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface2) !important;
    font-size: 0.875rem !important;
}

.stProgress > div > div {
    background: #e2e8f0 !important;
    border-radius: 100px !important;
    height: 6px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #475569, #64748b) !important;
    border-radius: 100px !important;
}

div[data-baseweb="tab"] {
    border-radius: 10px !important;
}

.stDataFrame { border-radius: var(--radius) !important; overflow: hidden !important; }

@media (max-width: 768px) {
    .stat-card .value { font-size:1.3rem !important; }
    .page-header h1 { font-size:1.35rem !important; }
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# API / DATA
# ═══════════════════════════════════════════════════════════════════════════════
def api(acao, aba, dados=None):
    try:
        if acao == "post":
            r = requests.post(API_URL, json={"aba": aba, "valores": dados}, timeout=15)
        elif acao == "delete":
            r = requests.delete(API_URL, params={"aba": aba, "id": dados}, timeout=15)
        else:
            r = requests.get(API_URL, params={"acao": acao, "aba": aba}, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        st.error(f"Erro de conexao: {e}")
    return None


def ler(aba):
    dados = api("ler", aba)
    return pd.DataFrame(dados) if dados and isinstance(dados, list) else pd.DataFrame()


def escrever(aba, valores):
    return api("post", aba, valores)


def excluir(aba, id):
    return api("delete", aba, id)


def next_id(df):
    if df.empty: return "1"
    return str(pd.to_numeric(df["ID"], errors="coerce").fillna(0).astype(int).max() + 1)


def safe_num(s):
    return pd.to_numeric(s, errors="coerce").fillna(0)


MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sb-brand">
            <h1>💰 Financas do Casal</h1>
            <span>Controle financeiro em dupla</span>
            <hr>
        </div>
        """, unsafe_allow_html=True)

        menu = st.radio(
            "nav",
            ["🏠  Dashboard", "➕  Nova Transacao", "📋  Transacoes",
             "📊  Relatorios", "🎯  Metas", "📁  Categorias", "📖  Manual"],
            label_visibility="collapsed"
        )
        return menu


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: stat card HTML
# ═══════════════════════════════════════════════════════════════════════════════
def stat_card(label, value, badge_text="", badge_color="", stripe=""):
    b = f'<div class="badge {badge_color}">{badge_text}</div>' if badge_text else ''
    s = f'<div class="stripe {stripe}"></div>' if stripe else ''
    return f"""<div class="stat-card">
        {s}
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        {b}
    </div>"""


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    df = ler("Transacoes")
    now = datetime.now()

    st.markdown("""
    <div class="page-header">
        <h1>Dashboard</h1>
        <p>Visao geral das suas finances</p>
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        mf = st.selectbox("Mes", range(1, 13), index=now.month - 1, format_func=lambda x: MESES[x-1], key="d_m")
    with fc2:
        af = st.selectbox("Ano", range(2024, 2031), index=now.year - 2024, key="d_a")

    rec = desp = saldo = 0
    dm = pd.DataFrame()

    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        df["Valor"] = safe_num(df["Valor"])
        dm = df[(df["Data"].dt.month == mf) & (df["Data"].dt.year == af)]
        rec = dm[dm["Tipo"] == "Receita"]["Valor"].sum()
        desp = dm[dm["Tipo"] == "Despesa"]["Valor"].sum()
        saldo = rec - desp

    # ── stat cards via HTML ──
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(stat_card("Receitas", f"R$ {rec:,.2f}", f"▲ {MESES[mf-1]}", "green", "green"), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card("Despesas", f"R$ {desp:,.2f}", f"▼ {MESES[mf-1]}", "red", "red"), unsafe_allow_html=True)
    with c3:
        s_label = "Saldo Positivo" if saldo >= 0 else "Saldo Negativo"
        s_color = "green" if saldo >= 0 else "red"
        s_icon  = "▲" if saldo >= 0 else "▼"
        st.markdown(stat_card("Saldo", f"R$ {saldo:,.2f}", f"{s_icon} {MESES[mf-1]}", s_color, "blue"), unsafe_allow_html=True)

    if not dm.empty:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        col_charts, col_recent = st.columns([5, 4])

        with col_charts:
            c_a, c_b = st.columns(2)
            with c_a:
                with st.container():
                    st.markdown("<div class='panel'><div class='panel-title'>Por Categoria</div>", unsafe_allow_html=True)
                    dc = dm[dm["Tipo"] == "Despesa"].groupby("Categoria")["Valor"].sum().sort_values(ascending=False)
                    if not dc.empty:
                        st.bar_chart(dc, height=220)
                    else:
                        st.markdown("<div class='empty-state'><p>Nenhuma despesa</p></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            with c_b:
                with st.container():
                    st.markdown("<div class='panel'><div class='panel-title'>Receita vs Despesa</div>", unsafe_allow_html=True)
                    rt = dm.groupby("Tipo")["Valor"].sum()
                    if not rt.empty:
                        st.bar_chart(rt, height=220)
                    st.markdown("</div>", unsafe_allow_html=True)

        with col_recent:
            with st.container():
                st.markdown("<div class='panel'><div class='panel-title'>Ultimas Transacoes</div>", unsafe_allow_html=True)
                ultimas = dm.sort_values("Data", ascending=False).head(8)
                for _, row in ultimas.iterrows():
                    chip_cls = "receita" if row["Tipo"] == "Receita" else "despesa"
                    icone = "↑" if row["Tipo"] == "Receita" else "↓"
                    st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid #f1f5f9;">
                        <div>
                            <div style="font-weight:600; font-size:0.85rem; color:#0f172a;">{row['Descricao']}</div>
                            <div style="font-size:0.75rem; color:#94a3b8;">{row['Responsavel']} · {row['Categoria']} · {str(row['Data'])[:10]}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-weight:700; font-size:0.85rem; color:{'#22c55e' if row['Tipo']=='Receita' else '#ef4444'};">{icone} R$ {row['Valor']:,.2f}</div>
                            <span class="chip {chip_cls}">{row['Tipo']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# NOVA TRANSACAO
# ═══════════════════════════════════════════════════════════════════════════════
def page_nova():
    st.markdown("""
    <div class="page-header">
        <h1>Nova Transacao</h1>
        <p>Registre uma receita ou despesa</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_nova", clear_on_submit=True):
        st.markdown("<div class='panel'><div class='panel-title'>Preencha os dados</div>", unsafe_allow_html=True)

        cats = ler("Categorias")

        c1, c2 = st.columns(2)
        data = c1.date_input("📅 Data", value=date.today())
        tipo = c2.selectbox("📌 Tipo", ["Receita", "Despesa"])

        cat_list = cats[cats["Tipo"] == tipo]["Nome"].tolist() if not cats.empty else ["Geral"]
        if not cat_list: cat_list = ["Geral"]

        categoria = st.selectbox("📂 Categoria", cat_list)
        desc = st.text_input("📝 Descricao", placeholder="Ex: Supermercado, Freelance, Conta de luz...")

        c3, c4 = st.columns(2)
        valor = c3.number_input("💰 Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
        parcelas = c4.number_input("🔢 Parcelas", min_value=1, max_value=48, value=1)

        resp = st.text_input("👤 Responsavel", placeholder="Quem pagou / recebeu?")

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        if st.form_submit_button("💾  Salvar Transacao", type="primary", use_container_width=True):
            if desc and valor > 0 and resp:
                df_t = ler("Transacoes")
                res = escrever("Transacoes", [
                    next_id(df_t), data.strftime("%Y-%m-%d"), tipo, categoria,
                    desc, str(valor), str(parcelas), resp
                ])
                if res and res.get("status") == "ok":
                    st.success("✅ Transacao salva!")
                    st.rerun()
                else:
                    st.error("Erro ao salvar")
            else:
                st.warning("Preencha todos os campos.")

        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TRANSACOES
# ═══════════════════════════════════════════════════════════════════════════════
def page_transacoes():
    st.markdown("""
    <div class="page-header">
        <h1>Transacoes</h1>
        <p>Visualize, filtre e gerencie seus registros</p>
    </div>
    """, unsafe_allow_html=True)

    df = ler("Transacoes")
    if df.empty:
        st.markdown("""<div class="empty-state"><div class="icon">📋</div><p>Nenhuma transacao cadastrada</p></div>""", unsafe_allow_html=True)
        return

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Valor"] = safe_num(df["Valor"])

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Filtros</div>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        tf = c1.selectbox("Tipo", ["Todos", "Receita", "Despesa"])
        cf = c2.selectbox("Categoria", ["Todas"] + sorted(df["Categoria"].dropna().unique()))
        rf = c3.selectbox("Responsavel", ["Todos"] + sorted(df["Responsavel"].dropna().unique()))
        busca = c4.text_input("🔎 Buscar", placeholder="Descricao...")
        st.markdown("</div>", unsafe_allow_html=True)

    f = df.copy()
    if tf != "Todos": f = f[f["Tipo"] == tf]
    if cf != "Todas": f = f[f["Categoria"] == cf]
    if rf != "Todos": f = f[f["Responsavel"] == rf]
    if busca: f = f[f["Descricao"].str.contains(busca, case=False, na=False)]

    total = f["Valor"].sum()
    rec_f = f[f["Tipo"] == "Receita"]["Valor"].sum()
    desp_f = f[f["Tipo"] == "Despesa"]["Valor"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(stat_card("Registros", str(len(f)), "", "", ""), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card("Receitas", f"R$ {rec_f:,.2f}", "", "green", "green"), unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card("Despesas", f"R$ {desp_f:,.2f}", "", "red", "red"), unsafe_allow_html=True)
    with c4:
        s_c = "green" if total >= 0 else "red"
        st.markdown(stat_card("Total", f"R$ {total:,.2f}", "", s_c, "blue"), unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown(f"<div class='panel'><div class='panel-title'>Registros ({len(f)})</div>", unsafe_allow_html=True)
        st.dataframe(
            f.sort_values("Data", ascending=False)[["ID","Data","Tipo","Categoria","Descricao","Valor","Parcelas","Responsavel"]].reset_index(drop=True),
            use_container_width=True, hide_index=True, height=min(len(f) * 40 + 60, 450)
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Excluir Registro</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([4, 1])
        id_ex = c1.text_input("ID", placeholder="Digite o ID do registro...", key="excl_id", label_visibility="collapsed")
        if c2.button("🗑️ Excluir", type="secondary", use_container_width=True):
            if id_ex:
                res = excluir("Transacoes", id_ex)
                if res and res.get("status") == "ok":
                    st.success("✅ Registro excluido!")
                    st.rerun()
                else:
                    st.error("ID nao encontrado")
            else:
                st.warning("Informe o ID")
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# RELATORIOS
# ═══════════════════════════════════════════════════════════════════════════════
def page_relatorios():
    st.markdown("""
    <div class="page-header">
        <h1>Relatorios</h1>
        <p>Analise detalhada das suas finances</p>
    </div>
    """, unsafe_allow_html=True)

    df = ler("Transacoes")
    if df.empty:
        st.markdown("""<div class="empty-state"><div class="icon">📊</div><p>Sem dados para gerar relatorios</p></div>""", unsafe_allow_html=True)
        return

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Valor"] = safe_num(df["Valor"])
    df["MesAno"] = df["Data"].dt.to_period("M").astype(str)

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Resumo Mensal</div>", unsafe_allow_html=True)
        r = df.groupby(["MesAno", "Tipo"])["Valor"].sum().unstack(fill_value=0)
        if "Receita" in r.columns and "Despesa" in r.columns:
            r["Saldo"] = r["Receita"] - r["Despesa"]
        st.dataframe(r, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container():
            st.markdown("<div class='panel'><div class='panel-title'>Top Despesas por Categoria</div>", unsafe_allow_html=True)
            d = df[df["Tipo"] == "Despesa"].groupby("Categoria")["Valor"].sum().sort_values(ascending=True)
            if not d.empty:
                st.bar_chart(d, height=280)
            st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        with st.container():
            st.markdown("<div class='panel'><div class='panel-title'>Por Responsavel</div>", unsafe_allow_html=True)
            p = df.groupby(["Responsavel", "Tipo"])["Valor"].sum().unstack(fill_value=0)
            if not p.empty:
                st.dataframe(p, use_container_width=True)
                st.bar_chart(p, height=180)
            st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Evolucao Mensal</div>", unsafe_allow_html=True)
        e = df.groupby("MesAno")["Valor"].sum()
        if not e.empty:
            st.area_chart(e, height=250)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# METAS
# ═══════════════════════════════════════════════════════════════════════════════
def page_metas():
    st.markdown("""
    <div class="page-header">
        <h1>Metas Financeiras</h1>
        <p>Defina objetivos e acompanhe o progresso</p>
    </div>
    """, unsafe_allow_html=True)

    df = ler("Metas")

    with st.container():
        with st.form("form_meta", clear_on_submit=True):
            st.markdown("<div class='panel'><div class='panel-title'>Nova Meta</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            nome = c1.text_input("🏷️ Nome", placeholder="Ex: Reserva de Emergencia...")
            va = c2.number_input("🎯 Valor Alvo (R$)", min_value=1.0, step=100.0, format="%.2f")
            pz = c1.date_input("📅 Prazo", value=date.today())
            vat = c2.number_input("💰 Valor Atual (R$)", min_value=0.0, step=10.0, format="%.2f")
            if st.form_submit_button("💾  Criar Meta", type="primary", use_container_width=True):
                if nome and va > 0:
                    res = escrever("Metas", [next_id(df), nome, str(va), str(vat), pz.strftime("%Y-%m-%d")])
                    if res and res.get("status") == "ok":
                        st.success("✅ Meta criada!")
                        st.rerun()
                    else:
                        st.error("Erro ao salvar")
            st.markdown("</div>", unsafe_allow_html=True)

    if not df.empty:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        df["ValorAlvo"] = safe_num(df["ValorAlvo"])
        df["ValorAtual"] = safe_num(df["ValorAtual"])

        # summary stats
        total_alvo = df["ValorAlvo"].sum()
        total_atual = df["ValorAtual"].sum()
        pct_geral = min(total_atual / total_alvo, 1.0) * 100 if total_alvo > 0 else 0
        concluidas = len(df[df["ValorAtual"] >= df["ValorAlvo"]])

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(stat_card("Total Alvo", f"R$ {total_alvo:,.2f}", "", "", "blue"), unsafe_allow_html=True)
        with c2:
            st.markdown(stat_card("Total Alcancado", f"R$ {total_atual:,.2f}", "", "", "green"), unsafe_allow_html=True)
        with c3:
            st.markdown(stat_card("Concluidas", f"{concluidas}/{len(df)}", f"{pct_geral:.0f}% do total", "green" if concluidas == len(df) else "blue", "blue"), unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        for _, m in df.iterrows():
            pct = min(m["ValorAtual"] / m["ValorAlvo"], 1.0) * 100 if m["ValorAlvo"] > 0 else 0
            pct_cls = "done" if pct >= 100 else "wip"
            icon = "✅" if pct >= 100 else "🎯"

            with st.container():
                st.markdown(f"""
                <div class="goal-card">
                    <div class="goal-head">
                        <span class="goal-name">{icon} {m['Nome']}</span>
                        <span class="goal-pct {pct_cls}">{pct:.0f}%</span>
                    </div>
                    <div class="goal-values">R$ {m['ValorAtual']:,.2f} / R$ {m['ValorAlvo']:,.2f}</div>
                    <div class="goal-due">📅 Prazo: {m.get('Prazo','N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
                if pct < 100:
                    st.progress(pct / 100)


# ═══════════════════════════════════════════════════════════════════════════════
# CATEGORIAS
# ═══════════════════════════════════════════════════════════════════════════════
def page_categorias():
    st.markdown("""
    <div class="page-header">
        <h1>Categorias</h1>
        <p>Gerencie as categorias de receitas e despesas</p>
    </div>
    """, unsafe_allow_html=True)

    df = ler("Categorias")

    if not df.empty:
        rec_count = len(df[df["Tipo"] == "Receita"]) if "Tipo" in df.columns else 0
        desp_count = len(df[df["Tipo"] == "Despesa"]) if "Tipo" in df.columns else 0

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(stat_card("Total", str(len(df)), "", "", ""), unsafe_allow_html=True)
        with c2:
            st.markdown(stat_card("Receitas", str(rec_count), "", "green", "green"), unsafe_allow_html=True)
        with c3:
            st.markdown(stat_card("Despesas", str(desp_count), "", "red", "red"), unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='panel'><div class='panel-title'>Cadastradas</div>", unsafe_allow_html=True)
            # custom display
            for _, row in df.iterrows():
                chip_cls = "receita" if row.get("Tipo") == "Receita" else "despesa"
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:0.65rem 0; border-bottom:1px solid #f1f5f9;">
                    <div style="font-weight:600; font-size:0.9rem; color:#0f172a;">{row.get('Nome','')}</div>
                    <span class="chip {chip_cls}">{row.get('Tipo','')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        with st.form("form_cat", clear_on_submit=True):
            st.markdown("<div class='panel'><div class='panel-title'>Adicionar Categoria</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            n = c1.text_input("🏷️ Nome", placeholder="Ex: Gasolina...")
            t = c2.selectbox("📌 Tipo", ["Receita", "Despesa"])
            if st.form_submit_button("💾  Adicionar", type="primary", use_container_width=True):
                if n:
                    res = escrever("Categorias", [next_id(df), n, t])
                    if res and res.get("status") == "ok":
                        st.success("✅ Categoria adicionada!")
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar")
            st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MANUAL
# ═══════════════════════════════════════════════════════════════════════════════
def page_manual():
    st.markdown("""
    <div class="page-header">
        <h1>Manual do Usuario</h1>
        <p>Guia completo de configuracao e uso do sistema</p>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("1", "Criar Planilha", "Crie uma planilha em branco no Google Sheets e nomeie como 'Financas Casal'."),
        ("2", "Executar Apps Script", "Abra a planilha, va em Extensões > Apps Script. Cole todo o codigo do arquivo apps_script.js, salve e execute a funcao SetupBancoDados (botaozinho verde ▶). Autorize as permissoes quando solicitado."),
        ("3", "Implantar Web App", "No Apps Script, va em Implantar > Nova implantacao. Selecione: Tipo = Aplicativo da web, Executar como = Eu, Quem tem acesso = Qualquer pessoa. Clique em Implantar e copie a URL gerada."),
        ("4", "Configurar .env", "Na pasta do projeto, crie o arquivo .env com o conteudo:\nAPI_URL=https://script.google.com/macros/s/SUA_URL/exec"),
        ("5", "Instalar e Rodar", "No terminal, execute:\npip install -r requirements.txt\nstreamlit run app.py\n\nAcesse http://localhost:8501"),
    ]

    for num, title, desc in steps:
        st.markdown(f"""
        <div class="panel" style="display:flex; gap:1rem; align-items:flex-start;">
            <div style="flex-shrink:0; width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#475569,#64748b); color:white; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">{num}</div>
            <div>
                <div style="font-weight:700; color:#0f172a; font-size:0.95rem; margin-bottom:0.25rem;">{title}</div>
                <div style="font-size:0.85rem; color:#475569; line-height:1.6;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Arquitetura do Sistema</div>", unsafe_allow_html=True)
        st.markdown("""
        ```
        Streamlit (app.py)                    Google Sheets
             │                                     ▲
             │    GET (ler)                        │
             ├────────────────────► Apps Script    │
             │    POST (escrever)     Web App  ────┘
             ├────────────────────►     (doGet/doPost)
             │    DELETE (excluir)
             └────────────────────►
        ```
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Estrutura da Planilha</div>", unsafe_allow_html=True)
        st.markdown("""
        | Aba | Colunas |
        |-----|---------|
        | **Categorias** | ID, Nome, Tipo |
        | **Transacoes** | ID, Data, Tipo, Categoria, Descricao, Valor, Parcelas, Responsavel |
        | **Metas** | ID, Nome, ValorAlvo, ValorAtual, Prazo |
        | **Config** | Chave, Valor |
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='panel'><div class='panel-title'>Dicas</div>", unsafe_allow_html=True)
        tips = [
            "Use nomes consistentes no campo Responsavel (ex: 'Joao' e 'Maria')",
            "Cadastre categorias personalizadas antes de lancar transacoes",
            "Acompanhe as metas mensalmente para manter o foco",
            "Use os filtros nos relatorios para analises especificas",
            "O campo Parcelas ajuda a rastrear compras parceladas",
        ]
        for tip in tips:
            st.markdown(f"**•** {tip}")
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    if not API_URL or "SEU_ID" in API_URL:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem;">
            <div style="font-size:4rem; margin-bottom:1rem;">⚙️</div>
            <h2 style="color:#0f172a; font-weight:800;">Configuracao Necessaria</h2>
            <p style="color:#64748b; font-size:0.95rem; max-width:500px; margin:0 auto;">
                Configure o arquivo <code>.env</code> com a URL do Web App do Apps Script.<br><br>
                Implantar > Nova implantacao > Aplicativo da web
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    menu = sidebar()

    pages = {
        "🏠  Dashboard": page_dashboard,
        "➕  Nova Transacao": page_nova,
        "📋  Transacoes": page_transacoes,
        "📊  Relatorios": page_relatorios,
        "🎯  Metas": page_metas,
        "📁  Categorias": page_categorias,
        "📖  Manual": page_manual,
    }
    pages[menu]()


if __name__ == "__main__":
    main()