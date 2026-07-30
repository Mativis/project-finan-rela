import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Financas do Casal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "")
_http = requests.Session()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --bg:        #eef0f4;
    --surface:   #ffffff;
    --surface-2: #f4f5f8;
    --border:    #cbd5e1;
    --border-2:  #e2e8f0;
    --text:      #0f172a;
    --text-2:    #334155;
    --text-3:    #64748b;
    --brand:     #7c3aed;
    --brand-2:   #6d28d9;
    --brand-bg:  #f5f3ff;
    --brand-br:  #ddd6fe;
    --green:     #059669;
    --green-2:   #047857;
    --green-bg:  #ecfdf5;
    --green-br:  #a7f3d0;
    --red:       #dc2626;
    --red-2:     #b91c1c;
    --red-bg:    #fef2f2;
    --red-br:    #fecaca;
    --amber:     #d97706;
    --amber-bg:  #fffbeb;
    --amber-br:  #fde68a;
    --radius:    8px;
    --radius-l:  14px;
    --radius-xl: 18px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
    --shadow:    0 2px 8px rgba(0,0,0,0.07);
    --shadow-md: 0 6px 20px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 40px rgba(0,0,0,0.14);
    --t:         0.2s cubic-bezier(0.4,0,0.2,1);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
html, body, .stApp { background: var(--bg) !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(185deg, #080c18 0%, #141a2e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] .stMarkdown * { color: #94a3b8 !important; }
section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; margin: 1rem 0 !important; }

.sb-brand {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 0.5rem;
}
.sb-brand .logo {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #7c3aed, #a21caf);
    border-radius: 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 6px 18px rgba(124,58,237,0.4);
}
.sb-brand h1 {
    color: #f8fafc !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    margin: 0 0 0.2rem !important;
}
.sb-brand span {
    color: #64748b !important;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.nav-section {
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: #475569;
    text-transform: uppercase;
    padding: 0 0.85rem;
    margin: 1.5rem 0 0.35rem 0;
}
.nav-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 0.5rem 0.85rem;
}

section[data-testid="stSidebar"] .stButton > div > button {
    background: transparent !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.55rem 0.85rem !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
    margin: 0 !important;
}
section[data-testid="stSidebar"] .stButton > div > button:hover {
    background: rgba(124,58,237,0.08) !important;
    border-left-color: rgba(124,58,237,0.3) !important;
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stButton > div > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > div > button[data-testid="stBaseButton-primary"] {
    background: rgba(124,58,237,0.15) !important;
    border-left-color: #7c3aed !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] .stButton > div > button[kind="primary"]:hover {
    background: rgba(124,58,237,0.2) !important;
}

.sb-footer {
    position: absolute;
    bottom: 1rem;
    left: 1rem;
    right: 1rem;
    padding: 1rem 0.75rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    text-align: center;
}
.sb-footer p {
    font-size: 0.62rem !important;
    color: #475569 !important;
    letter-spacing: 0.03em;
    margin: 0 !important;
}

/* ── Page header ── */
.page-header {
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1rem;
}
.page-header .left h1 {
    font-size: 1.7rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.04em;
    color: var(--text) !important;
    margin: 0 !important;
    line-height: 1.2;
}
.page-header .left p {
    color: var(--text-3) !important;
    font-size: 0.85rem;
    margin: 0.25rem 0 0 0;
    font-weight: 400;
}
.page-header .right { flex-shrink: 0; }

/* ── Card ── */
.card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 1.5rem 1.75rem;
    box-shadow: var(--shadow);
    transition: all var(--t);
    position: relative;
    overflow: hidden;
}
.card:hover { box-shadow: var(--shadow-lg); transform: translateY(-3px); }
.card .accent {
    position: absolute; top: 0; left: 0;
    width: 5px; height: 100%;
    border-radius: 0 3px 3px 0;
}
.card .accent.green  { background: linear-gradient(180deg, #059669, #34d399); }
.card .accent.red    { background: linear-gradient(180deg, #dc2626, #f87171); }
.card .accent.brand  { background: linear-gradient(180deg, #7c3aed, #a21caf); }
.card .accent.amber  { background: linear-gradient(180deg, #d97706, #fbbf24); }
.card .card-body { padding-left: 0.35rem; }
.card .card-label {
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-3);
    margin-bottom: 0.35rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card .card-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.04em;
    line-height: 1.2;
}
.card .card-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 100px;
    margin-top: 0.5rem;
}
.card .card-badge.green { background: var(--green-bg); color: var(--green-2); border: 1.5px solid var(--green-br); }
.card .card-badge.red   { background: var(--red-bg);   color: var(--red-2);   border: 1.5px solid var(--red-br); }
.card .card-badge.brand { background: var(--brand-bg); color: var(--brand-2); border: 1.5px solid var(--brand-br); }
.card .card-badge.amber { background: var(--amber-bg); color: var(--amber);   border: 1.5px solid var(--amber-br); }

/* ── Panel ── */
.panel {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 1.5rem 1.75rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.25rem;
    transition: all var(--t);
}
.panel-title {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    font-size: 0.73rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-3);
    margin-bottom: 1.25rem;
    padding-bottom: 0.85rem;
    border-bottom: 2px solid var(--border-2);
}
.panel-title .icon {
    width: 26px; height: 26px;
    background: var(--brand-bg);
    border-radius: 7px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    color: var(--brand);
    flex-shrink: 0;
}

/* ── Chip ── */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.7rem;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    white-space: nowrap;
}
.chip.receita { background: var(--green-bg); color: var(--green-2); border: 1.5px solid var(--green-br); }
.chip.despesa { background: var(--red-bg);   color: var(--red-2);   border: 1.5px solid var(--red-br); }

/* ── Transaction row ── */
.tx-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0.5rem;
    border-bottom: 1.5px solid var(--border-2);
    transition: var(--t);
    border-radius: 6px;
    margin: 0 -0.5rem;
}
.tx-row:hover { background: var(--surface-2); padding-left: 1rem; }
.tx-row:last-child { border-bottom: none; }
.tx-row .tx-info .tx-desc {
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--text);
    margin-bottom: 0.15rem;
}
.tx-row .tx-info .tx-meta {
    font-size: 0.7rem;
    color: var(--text-3);
}
.tx-row .tx-amount {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
}
.tx-row .tx-amount .tx-value {
    font-weight: 700;
    font-size: 0.88rem;
}
.tx-row .tx-amount .tx-type { margin-top: 0.2rem; }

/* ── Goal card ── */
.goal-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-xl);
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.85rem;
    box-shadow: var(--shadow);
    transition: all var(--t);
}
.goal-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.goal-card .goal-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}
.goal-card .goal-name {
    font-weight: 800;
    font-size: 0.9rem;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.goal-card .goal-pct {
    font-weight: 700;
    font-size: 0.8rem;
    padding: 0.25rem 0.7rem;
    border-radius: 100px;
}
.goal-card .goal-pct.done { background: var(--green-bg); color: var(--green-2); border: 1.5px solid var(--green-br); }
.goal-card .goal-pct.wip  { background: var(--brand-bg); color: var(--brand-2); border: 1.5px solid var(--brand-br); }
.goal-card .goal-values {
    font-size: 0.8rem;
    color: var(--text-2);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.35rem;
}
.goal-card .goal-due {
    font-size: 0.7rem;
    color: var(--text-3);
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3.5rem 1.5rem;
    color: var(--text-3);
    background: var(--surface);
    border: 1.5px dashed var(--border);
    border-radius: var(--radius-xl);
}
.empty-state .icon {
    font-size: 2.8rem;
    margin-bottom: 0.75rem;
    opacity: 0.35;
}
.empty-state p { font-size: 0.9rem; font-weight: 600; color: var(--text-2); margin: 0; }
.empty-state .sub { font-size: 0.78rem; color: var(--text-3); margin-top: 0.3rem; }

/* ── Divider ── */
.divider { border: none; border-top: 2px solid var(--border-2); margin: 1.25rem 0; }

/* ── Overrides ── */
.stMetric { background: transparent !important; border: none !important; padding: 0 !important; }
.stMetric label { display: none !important; }
.stMetric [data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}
.stMetric [data-testid="stMetricDelta"] { font-size: 0.75rem !important; font-weight: 600 !important; }

.stButton > div > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.2s ease !important;
}
.stButton > div > button[kind="primary"],
.stButton > div > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #7c3aed, #a21caf) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 3px 10px rgba(124,58,237,0.35) !important;
}
.stButton > div > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(124,58,237,0.5) !important;
    transform: translateY(-2px) !important;
}
.stButton > div > button[kind="secondary"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-2) !important;
}
.stButton > div > button[kind="secondary"]:hover {
    background: var(--surface-2) !important;
    border-color: #94a3b8 !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stSelectbox > div > div > div {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface) !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,0.15) !important;
    background: var(--surface) !important;
}
.stSelectbox > div > div > div:focus-within {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 4px rgba(124,58,237,0.15) !important;
}
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    background: var(--surface) !important;
    font-size: 0.85rem !important;
    box-shadow: var(--shadow-sm) !important;
}

.stProgress > div > div {
    background: var(--border-2) !important;
    border-radius: 100px !important;
    height: 8px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #a21caf) !important;
    border-radius: 100px !important;
}

div[data-baseweb="tab"] { border-radius: 10px !important; }

.stDataFrame {
    border-radius: var(--radius-l) !important;
    overflow: hidden !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stForm { border: none !important; background: transparent !important; padding: 0 !important; }
.stAlert { border-radius: 12px !important; border: 1px solid !important; }

.stSelectbox label, .stNumberInput label, .stDateInput label, .stTextInput label {
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    color: var(--text-2) !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
    .card .card-value { font-size: 1.25rem !important; }
    .page-header { flex-direction: column; align-items: flex-start; }
    .page-header .left h1 { font-size: 1.35rem !important; }
    .sb-brand { padding: 1.5rem 0.5rem 1rem; }
    section[data-testid="stSidebar"] [data-baseweb="radio"] label { font-size: 0.76rem !important; padding: 0.45rem 0.6rem !important; }
}
</style>
""", unsafe_allow_html=True)

MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

def api(metodo, aba, dados=None):
    try:
        if metodo == "post":
            r = _http.post(API_URL, json={"aba": aba, "valores": dados}, timeout=30)
        elif metodo == "delete":
            r = _http.delete(API_URL, params={"aba": aba, "id": dados}, timeout=30)
        else:
            r = _http.get(API_URL, params={"acao": metodo, "aba": aba}, timeout=30)

        if r.status_code == 200:
            j = r.json()
            if isinstance(j, dict) and j.get("_httpCode") and j["_httpCode"] >= 400:
                erro = j.get("erro", j.get("mensagem", f"Erro {j['_httpCode']}"))
                st.error(f"❌ Servidor: {erro}")
                return None
            return j
        else:
            try:
                msg = r.json().get("erro", r.text[:200]) if r.text else f"HTTP {r.status_code}"
            except Exception:
                msg = f"HTTP {r.status_code}"
            st.error(f"❌ {msg}")
            return None

    except requests.exceptions.Timeout:
        st.error("⏱️ Tempo limite excedido. Verifique se o Web App esta respondendo.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Nao foi possivel conectar. Verifique a URL do Web App.")
    except requests.exceptions.JSONDecodeError:
        st.error("📄 Resposta invalida do servidor. Verifique a URL do Web App.")
    except Exception as e:
        st.error(f"❌ Erro: {e}")
    return None

def ler(aba):
    dados = api("ler", aba)
    return pd.DataFrame(dados) if dados and isinstance(dados, list) else pd.DataFrame()

def escrever(aba, valores):
    return api("post", aba, valores)

def excluir(aba, id_registro):
    return api("delete", aba, id_registro)

def proximo_id(df):
    if df.empty:
        return "1"
    ids = pd.to_numeric(df["ID"], errors="coerce").fillna(0).astype(int)
    return str(ids.max() + 1)

def safe_num(s):
    return pd.to_numeric(s, errors="coerce").fillna(0)

def card(label, value, badge="", color="brand"):
    c = color
    b = f'<span class="card-badge {c}">{badge}</span>' if badge else ""
    return f"""
    <div class="card">
        <div class="accent {c}"></div>
        <div class="card-body">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
            {b}
        </div>
    </div>
    """

def pagetitle(title, subtitle=""):
    st.markdown(f"""
    <div class="page-header">
        <div class="left">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

def nav_btn(label, icon, active):
    kind = "primary" if active else "secondary"
    return st.sidebar.button(
        f"{icon}  {label}",
        key=f"nv_{label.replace(' ','')}",
        type=kind,
        use_container_width=True,
    )

def sidebar():
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    with st.sidebar:
        st.markdown("""
        <div class="sb-brand">
            <div class="logo">💰</div>
            <h1>Financas do Casal</h1>
            <span>Controle financeiro em dupla</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="nav-section">Principal</div>', unsafe_allow_html=True)
        if nav_btn("Dashboard", "🏠", st.session_state.page == "Dashboard"):
            st.session_state.page = "Dashboard"; st.rerun()
        if nav_btn("Relatorios", "📊", st.session_state.page == "Relatorios"):
            st.session_state.page = "Relatorios"; st.rerun()

        st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)
        st.markdown('<div class="nav-section">Gerenciamento</div>', unsafe_allow_html=True)
        if nav_btn("Nova Transacao", "➕", st.session_state.page == "Nova Transacao"):
            st.session_state.page = "Nova Transacao"; st.rerun()
        if nav_btn("Transacoes", "📋", st.session_state.page == "Transacoes"):
            st.session_state.page = "Transacoes"; st.rerun()
        if nav_btn("Metas", "🎯", st.session_state.page == "Metas"):
            st.session_state.page = "Metas"; st.rerun()
        if nav_btn("Categorias", "📁", st.session_state.page == "Categorias"):
            st.session_state.page = "Categorias"; st.rerun()

        st.markdown('<hr class="nav-divider">', unsafe_allow_html=True)
        st.markdown('<div class="nav-section">Suporte</div>', unsafe_allow_html=True)
        if nav_btn("Manual", "📖", st.session_state.page == "Manual"):
            st.session_state.page = "Manual"; st.rerun()

        st.markdown('<div class="sb-footer"><p>financasdocal.com.br</p></div>', unsafe_allow_html=True)

        return st.session_state.page

def panel(title, icon):
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title"><span class="icon">{icon}</span> {title}</div>
    """, unsafe_allow_html=True)
    return st.container()

def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)

def page_dashboard():
    df = ler("Transacoes")
    now = datetime.now()

    pagetitle("Dashboard", "Visao geral das suas financas")

    c1, c2 = st.columns(2)
    with c1:
        mes = st.selectbox("Mes", range(1, 13), index=now.month - 1, format_func=lambda x: MESES[x-1], key="d_mes")
    with c2:
        ano = st.selectbox("Ano", range(2024, 2031), index=now.year - 2024, key="d_ano")

    receitas = despesas = saldo = 0
    dm = pd.DataFrame()

    if not df.empty:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        df["Valor"] = safe_num(df["Valor"])
        dm = df[(df["Data"].dt.month == mes) & (df["Data"].dt.year == ano)]
        receitas = dm[dm["Tipo"] == "Receita"]["Valor"].sum()
        despesas = dm[dm["Tipo"] == "Despesa"]["Valor"].sum()
        saldo = receitas - despesas

    x, y, z = st.columns(3)
    with x:
        st.markdown(card("Receitas", f"R$ {receitas:,.2f}", f"▲ {MESES[mes-1]}", "green"), unsafe_allow_html=True)
    with y:
        st.markdown(card("Despesas", f"R$ {despesas:,.2f}", f"▼ {MESES[mes-1]}", "red"), unsafe_allow_html=True)
    with z:
        if saldo >= 0:
            st.markdown(card("Saldo", f"R$ {saldo:,.2f}", "▲ Positivo", "green"), unsafe_allow_html=True)
        else:
            st.markdown(card("Saldo", f"R$ {saldo:,.2f}", "▼ Negativo", "red"), unsafe_allow_html=True)

    if dm.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📊</div>
            <p>Nenhuma transacao neste mes</p>
            <div class="sub">Cadastre transacoes em "Nova Transacao" para ver graficos</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    esq, dir = st.columns([5, 4])

    with esq:
        a, b = st.columns(2)
        with a:
            with panel("Despesas por Categoria", "📊"):
                dc = dm[dm["Tipo"] == "Despesa"].groupby("Categoria")["Valor"].sum().sort_values(ascending=False)
                if not dc.empty:
                    st.bar_chart(dc, height=220, color="#7c3aed")
                else:
                    st.markdown('<div class="empty-state"><p>Sem despesas</p></div>', unsafe_allow_html=True)
            panel_end()

        with b:
            with panel("Receita vs Despesa", "📈"):
                rt = dm.groupby("Tipo")["Valor"].sum()
                if not rt.empty:
                    st.bar_chart(rt, height=220, color="#7c3aed")
            panel_end()

    with dir:
        with panel("Ultimas Transacoes", "🕐"):
            ultimas = dm.sort_values("Data", ascending=False).head(8)
            for _, row in ultimas.iterrows():
                tcls = "receita" if row["Tipo"] == "Receita" else "despesa"
                sinal = "+" if row["Tipo"] == "Receita" else "-"
                cor = "#059669" if row["Tipo"] == "Receita" else "#dc2626"
                dt = str(row["Data"])[:10] if pd.notna(row["Data"]) else ""
                st.markdown(f"""
                <div class="tx-row">
                    <div class="tx-info">
                        <div class="tx-desc">{row['Descricao']}</div>
                        <div class="tx-meta">{row['Responsavel']} &middot; {row['Categoria']} &middot; {dt}</div>
                    </div>
                    <div class="tx-amount">
                        <div class="tx-value" style="color:{cor};">{sinal} R$ {row['Valor']:,.2f}</div>
                        <span class="chip {tcls}">{row['Tipo']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        panel_end()

def page_nova():
    pagetitle("Nova Transacao", "Registre uma receita ou despesa")

    with st.form("form_nova", clear_on_submit=True):
        with panel("Dados da Transacao", "📝"):
            cats = ler("Categorias")

            c1, c2 = st.columns(2)
            data = c1.date_input("📅 Data", value=date.today())
            tipo = c2.selectbox("📌 Tipo", ["Receita", "Despesa"])

            cl = cats[cats["Tipo"] == tipo]["Nome"].tolist() if not cats.empty else ["Geral"]
            if not cl: cl = ["Geral"]

            c3, c4 = st.columns(2)
            categoria = c3.selectbox("📂 Categoria", cl)
            parcelas = c4.number_input("🔢 Parcelas", min_value=1, max_value=48, value=1)

            desc = st.text_input("📝 Descricao", placeholder="Ex: Supermercado, Freelance, Conta de luz...")

            c5, c6 = st.columns(2)
            valor = c5.number_input("💰 Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
            responsavel = c6.text_input("👤 Responsavel", placeholder="Quem pagou / recebeu?")

            st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

            if st.form_submit_button("💾  Salvar Transacao", type="primary", use_container_width=True):
                if not desc:
                    st.warning("⚠️ Informe a descricao")
                elif not responsavel:
                    st.warning("⚠️ Informe o responsavel")
                elif valor <= 0:
                    st.warning("⚠️ Informe um valor valido")
                else:
                    df_t = ler("Transacoes")
                    res = escrever("Transacoes", [
                        proximo_id(df_t), data.strftime("%Y-%m-%d"), tipo, categoria,
                        desc, str(valor), str(parcelas), responsavel
                    ])
                    if res and res.get("status") == "ok":
                        st.success("✅ Transacao salva com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar. Verifique a conexao com o Web App.")
        panel_end()

def page_transacoes():
    pagetitle("Transacoes", "Visualize, filtre e gerencie seus registros")

    df = ler("Transacoes")
    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📋</div>
            <p>Nenhuma transacao cadastrada</p>
            <div class="sub">Va em "Nova Transacao" para comecar a registrar</div>
        </div>
        """, unsafe_allow_html=True)
        return

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Valor"] = safe_num(df["Valor"])
    df["MesAno"] = df["Data"].dt.to_period("M").astype(str)

    with panel("Filtros", "🔍"):
        c1, c2, c3, c4 = st.columns(4)
        tf = c1.selectbox("Tipo", ["Todos", "Receita", "Despesa"])
        cf = c2.selectbox("Categoria", ["Todas"] + sorted(df["Categoria"].dropna().unique()))
        rf = c3.selectbox("Responsavel", ["Todos"] + sorted(df["Responsavel"].dropna().unique()))
        busca = c4.text_input("🔎 Buscar", placeholder="Descricao...")
    panel_end()

    flt = df.copy()
    if tf != "Todos": flt = flt[flt["Tipo"] == tf]
    if cf != "Todas": flt = flt[flt["Categoria"] == cf]
    if rf != "Todos": flt = flt[flt["Responsavel"] == rf]
    if busca: flt = flt[flt["Descricao"].str.contains(busca, case=False, na=False)]

    total = flt["Valor"].sum()
    rec_f = flt[flt["Tipo"] == "Receita"]["Valor"].sum()
    desp_f = flt[flt["Tipo"] == "Despesa"]["Valor"].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(card("Registros", str(len(flt)), color="brand"), unsafe_allow_html=True)
    with c2: st.markdown(card("Receitas", f"R$ {rec_f:,.2f}", color="green"), unsafe_allow_html=True)
    with c3: st.markdown(card("Despesas", f"R$ {desp_f:,.2f}", color="red"), unsafe_allow_html=True)
    with c4:
        cor = "green" if total >= 0 else "red"
        st.markdown(card("Saldo", f"R$ {total:,.2f}", color=cor), unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    with panel(f"Registros ({len(flt)})", "📄"):
        st.dataframe(
            flt.sort_values("Data", ascending=False)[["ID","Data","Tipo","Categoria","Descricao","Valor","Parcelas","Responsavel"]].reset_index(drop=True),
            use_container_width=True, hide_index=True, height=min(len(flt) * 40 + 60, 480)
        )
    panel_end()

    with panel("Excluir Registro", "🗑️"):
        c1, c2 = st.columns([4, 1])
        id_ex = c1.text_input("ID", placeholder="Digite o ID do registro...", label_visibility="collapsed")
        if c2.button("🗑️ Excluir", type="secondary", use_container_width=True):
            if id_ex:
                res = excluir("Transacoes", id_ex)
                if res and res.get("status") == "ok":
                    st.success("✅ Registro excluido!")
                    st.rerun()
                else:
                    st.error("❌ ID nao encontrado")
            else:
                st.warning("⚠️ Informe o ID")
    panel_end()

def page_relatorios():
    pagetitle("Relatorios", "Analise detalhada das suas financas")

    df = ler("Transacoes")
    if df.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">📊</div>
            <p>Sem dados para gerar relatorios</p>
            <div class="sub">Cadastre transacoes primeiro</div>
        </div>
        """, unsafe_allow_html=True)
        return

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df["Valor"] = safe_num(df["Valor"])
    df["MesAno"] = df["Data"].dt.to_period("M").astype(str)

    with panel("Resumo Mensal", "📅"):
        r = df.groupby(["MesAno", "Tipo"])["Valor"].sum().unstack(fill_value=0)
        if "Receita" in r.columns and "Despesa" in r.columns:
            r["Saldo"] = r["Receita"] - r["Despesa"]
            r["% Economia"] = (r["Saldo"] / r["Receita"] * 100).round(1).astype(str) + "%"
        st.dataframe(r, use_container_width=True)
    panel_end()

    c1, c2 = st.columns(2)
    with c1:
        with panel("Top Despesas por Categoria", "🏷️"):
            dc = df[df["Tipo"] == "Despesa"].groupby("Categoria")["Valor"].sum().sort_values(ascending=True)
            if not dc.empty:
                st.bar_chart(dc, height=280, color="#dc2626")
            else:
                st.markdown('<div class="empty-state"><p>Nenhuma despesa registrada</p></div>', unsafe_allow_html=True)
        panel_end()

    with c2:
        with panel("Por Responsavel", "👥"):
            pp = df.groupby(["Responsavel", "Tipo"])["Valor"].sum().unstack(fill_value=0)
            if not pp.empty:
                st.dataframe(pp, use_container_width=True)
                st.bar_chart(pp, height=180, color=["#7c3aed", "#dc2626"])
            else:
                st.markdown('<div class="empty-state"><p>Sem dados</p></div>', unsafe_allow_html=True)
        panel_end()

    with panel("Evolucao Mensal", "📈"):
        ev = df.groupby("MesAno")["Valor"].sum()
        if not ev.empty:
            st.area_chart(ev, height=250, color="#7c3aed")
    panel_end()

def page_metas():
    pagetitle("Metas Financeiras", "Defina objetivos e acompanhe o progresso")

    df = ler("Metas")

    with st.form("form_meta", clear_on_submit=True):
        with panel("Nova Meta", "🎯"):
            c1, c2 = st.columns(2)
            nome = c1.text_input("🏷️ Nome", placeholder="Ex: Reserva de Emergencia...")
            va = c2.number_input("🎯 Valor Alvo (R$)", min_value=1.0, step=100.0, format="%.2f")
            prazo = c1.date_input("📅 Prazo", value=date.today())
            vat = c2.number_input("💰 Valor Atual (R$)", min_value=0.0, step=10.0, format="%.2f")
            if st.form_submit_button("💾  Criar Meta", type="primary", use_container_width=True):
                if nome and va > 0:
                    res = escrever("Metas", [proximo_id(df), nome, str(va), str(vat), prazo.strftime("%Y-%m-%d")])
                    if res and res.get("status") == "ok":
                        st.success("✅ Meta criada com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar. Verifique a conexao.")
        panel_end()

    if not df.empty:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        df["ValorAlvo"] = safe_num(df["ValorAlvo"])
        df["ValorAtual"] = safe_num(df["ValorAtual"])

        talvo = df["ValorAlvo"].sum()
        tatual = df["ValorAtual"].sum()
        pctg = min(tatual / talvo, 1.0) * 100 if talvo > 0 else 0
        concluidas = len(df[df["ValorAtual"] >= df["ValorAlvo"]])

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(card("Total em Metas", f"R$ {talvo:,.2f}", color="brand"), unsafe_allow_html=True)
        with c2: st.markdown(card("Total Acumulado", f"R$ {tatual:,.2f}", color="green"), unsafe_allow_html=True)
        with c3:
            lbl = f"{concluidas} de {len(df)} concluidas"
            cor = "green" if concluidas == len(df) else "brand"
            st.markdown(card("Progresso", f"{pctg:.0f}%", lbl, cor), unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        for _, m in df.iterrows():
            pct = min(m["ValorAtual"] / m["ValorAlvo"], 1.0) * 100 if m["ValorAlvo"] > 0 else 0
            sc = "done" if pct >= 100 else "wip"
            ic = "✅" if pct >= 100 else "🎯"
            st.markdown(f"""
            <div class="goal-card">
                <div class="goal-head">
                    <span class="goal-name">{ic} {m['Nome']}</span>
                    <span class="goal-pct {sc}">{pct:.0f}%</span>
                </div>
                <div class="goal-values">R$ {m['ValorAtual']:,.2f} / R$ {m['ValorAlvo']:,.2f}</div>
                <div class="goal-due">📅 Prazo: {m.get('Prazo', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
            if pct < 100:
                st.progress(int(pct))

def page_categorias():
    pagetitle("Categorias", "Gerencie as categorias de receitas e despesas")

    df = ler("Categorias")

    if not df.empty and "Tipo" in df.columns:
        rc = len(df[df["Tipo"] == "Receita"])
        dc = len(df[df["Tipo"] == "Despesa"])

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(card("Total", str(len(df)), color="brand"), unsafe_allow_html=True)
        with c2: st.markdown(card("Receitas", str(rc), color="green"), unsafe_allow_html=True)
        with c3: st.markdown(card("Despesas", str(dc), color="red"), unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        with panel("Categorias Cadastradas", "📂"):
            for _, row in df.iterrows():
                cc = "receita" if row.get("Tipo") == "Receita" else "despesa"
                st.markdown(f"""
                <div class="tx-row">
                    <div class="tx-info">
                        <div class="tx-desc">{row.get('Nome','')}</div>
                    </div>
                    <span class="chip {cc}">{row.get('Tipo','')}</span>
                </div>
                """, unsafe_allow_html=True)
        panel_end()

    with st.form("form_cat", clear_on_submit=True):
        with panel("Adicionar Categoria", "➕"):
            c1, c2 = st.columns(2)
            nome = c1.text_input("🏷️ Nome", placeholder="Ex: Gasolina, Mercado...")
            tipo = c2.selectbox("📌 Tipo", ["Receita", "Despesa"])
            if st.form_submit_button("💾  Adicionar", type="primary", use_container_width=True):
                if nome:
                    pid = proximo_id(df) if not df.empty else "1"
                    res = escrever("Categorias", [pid, nome, tipo])
                    if res and res.get("status") == "ok":
                        st.success("✅ Categoria adicionada!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar")
        panel_end()

def page_manual():
    pagetitle("Manual do Usuario", "Guia completo de configuracao e uso do sistema")

    passos = [
        ("1", "Criar Planilha", "Crie uma planilha em branco no Google Sheets e nomeie como <strong>Financas Casal</strong>."),
        ("2", "Executar Apps Script", "Abra a planilha, va em <strong>Extensoes → Apps Script</strong>. Cole todo o codigo do arquivo <code>apps_script.js</code>, salve e execute a funcao <code>SetupBancoDados</code>. Autorize as permissoes."),
        ("3", "Implantar Web App", "No Apps Script, va em <strong>Implantar → Nova implantacao</strong>. Selecione: Tipo = Aplicativo da web, Executar como = Eu, Quem tem acesso = Qualquer pessoa. Copie a URL gerada."),
        ("4", "Configurar .env", "Na pasta do projeto, crie o arquivo <code>.env</code> com:<br><code>API_URL=https://script.google.com/macros/s/SUA_URL/exec</code>"),
        ("5", "Instalar e Rodar", "No terminal, execute:<br><code>pip install -r requirements.txt</code><br><code>streamlit run app.py</code><br><br>Acesse <strong>http://localhost:8501</strong>"),
    ]

    for num, titulo, desc in passos:
        st.markdown(f"""
        <div class="card" style="display:flex; gap:1.25rem; align-items:flex-start; margin-bottom:0.85rem; padding:1.25rem 1.5rem;">
            <div style="flex-shrink:0; width:38px; height:38px; border-radius:12px; background:linear-gradient(135deg,#7c3aed,#a21caf); color:white; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:1rem;">{num}</div>
            <div>
                <div style="font-weight:800; color:var(--text); font-size:0.95rem; margin-bottom:0.3rem;">{titulo}</div>
                <div style="font-size:0.85rem; color:var(--text-2); line-height:1.7;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    with panel("Arquitetura do Sistema", "🏗️"):
        st.markdown("""
        ```
        Streamlit (app.py)                    Google Sheets
             |                                     ▲
             |    GET / POST / DELETE               |
             ├────────────────────► Apps Script     │
             │    Web App API        ───────────────┘
             └────────────────────►   (doGet/doPost/doDelete)
        ```
        """)
    panel_end()

    with panel("Estrutura da Planilha", "📋"):
        st.markdown("""
        | **Aba** | **Colunas** |
        |---|---|
        | **Categorias** | ID, Nome, Tipo |
        | **Transacoes** | ID, Data, Tipo, Categoria, Descricao, Valor, Parcelas, Responsavel |
        | **Metas** | ID, Nome, ValorAlvo, ValorAtual, Prazo |
        | **Config** | Chave, Valor |
        """)
    panel_end()

    with panel("Dicas", "💡"):
        dicas = [
            "Use nomes consistentes no campo Responsavel (ex: 'Joao' e 'Maria')",
            "Cadastre categorias personalizadas antes de lancar transacoes",
            "Acompanhe as metas mensalmente para manter o foco",
            "Use os filtros nos relatorios para analises especificas",
            "O campo Parcelas ajuda a rastrear compras parceladas"
        ]
        for d in dicas:
            st.markdown(f"<div style='padding:0.35rem 0; color:var(--text-2); font-size:0.85rem; display:flex; align-items:center; gap:0.5rem;'><span style='color:var(--brand); font-weight:900;'>●</span> {d}</div>", unsafe_allow_html=True)
    panel_end()

def main():
    if not API_URL:
        st.markdown("""
        <div style="text-align:center; padding:5rem 1.5rem;">
            <div style="font-size:4rem; margin-bottom:1rem; opacity:0.5;">⚙️</div>
            <h2 style="color:#0f172a; font-weight:900; font-size:1.6rem; letter-spacing:-0.03em; margin-bottom:0.75rem;">Configuracao Necessaria</h2>
            <p style="color:#64748b; font-size:0.9rem; max-width:500px; margin:0 auto 2rem; line-height:1.6;">
                Para usar o sistema, voce precisa configurar a URL do Web App
                do Google Apps Script no arquivo <code style="background:#f1f5f9; padding:0.15rem 0.5rem; border-radius:6px; font-weight:600;">.env</code>
            </p>
            <div style="background:#f8fafc; border:1.5px solid #e2e8f0; border-radius:16px; padding:2rem 2.5rem; max-width:620px; margin:0 auto; text-align:left; font-size:0.88rem; color:#475569; line-height:1.9;">
                <strong style="color:#0f172a; font-size:0.95rem;">Passos rapidos:</strong><br>
                1. Crie uma planilha no <strong>Google Sheets</strong><br>
                2. <strong>Extensoes → Apps Script</strong> → cole o codigo de <code>apps_script.js</code><br>
                3. Execute <code>SetupBancoDados</code> e autorize as permissoes<br>
                4. <strong>Implantar → Nova implantacao</strong> → Aplicativo da web<br>
                5. Copie a URL e cole no <code>.env</code><br><br>
                <div style="background:#eef2ff; border:1px solid #c7d2fe; border-radius:10px; padding:0.75rem 1rem; margin-top:0.5rem;">
                    <code style="font-size:0.78rem; word-break:break-all;">API_URL=https://script.google.com/macros/s/SEU_ID/exec</code>
                </div>
            </div>
            <div style="margin-top:2rem;">
                <p style="font-size:0.78rem; color:#94a3b8;">Depois de configurar, atualize a pagina (F5)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    pagina = sidebar()

    paginas = {
        "Dashboard": page_dashboard,
        "Nova Transacao": page_nova,
        "Transacoes": page_transacoes,
        "Relatorios": page_relatorios,
        "Metas": page_metas,
        "Categorias": page_categorias,
        "Manual": page_manual,
    }

    with st.container():
        paginas[pagina]()

if __name__ == "__main__":
    main()
