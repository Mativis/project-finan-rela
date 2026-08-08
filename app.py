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

MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
MESES_COMPLETO = [
    "Janeiro","Fevereiro","Marco","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root, .stApp {
    --bg:        #f4f5f7;
    --surface:   #ffffff;
    --surface-2: #f8f9fb;
    --border:    #dfe3e8;
    --border-2:  #eef0f4;
    --text:      #1a1d21;
    --text-2:    #454f5b;
    --text-3:    #8c9196;
    --brand:     #1a56db;
    --brand-2:   #1648c0;
    --brand-bg:  #eef3ff;
    --brand-br:  #c7d7fe;
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
    --shadow:    0 1px 4px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.10);
}

@media (prefers-color-scheme: dark) {
    :root, .stApp {
        --bg:        #0f1115;
        --surface:   #1a1d23;
        --surface-2: #22252b;
        --border:    #2e3038;
        --border-2:  #26282f;
        --text:      #e8eaed;
        --text-2:    #b0b3b8;
        --text-3:    #72757a;
        --brand:     #3b82f6;
        --brand-2:   #60a5fa;
        --brand-bg:  #1e2433;
        --brand-br:  #2e3a5c;
        --green:     #34d399;
        --green-2:   #6ee7b7;
        --green-bg:  #14291e;
        --green-br:  #1f3d2e;
        --red:       #f87171;
        --red-2:     #fca5a5;
        --red-bg:    #2d1414;
        --red-br:    #4a2020;
        --amber:     #fbbf24;
        --amber-bg:  #2d2410;
        --amber-br:  #4a3a1a;
        --shadow:    0 1px 4px rgba(0,0,0,0.25);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.35);
        --shadow-lg: 0 8px 32px rgba(0,0,0,0.45);
    }
    .stApp header { background: #0f1115 !important; }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080b12 0%, #0e111a 100%) !important;
    }
    section[data-testid="stSidebar"] .stButton > div > button:hover { color: #e0e3e8 !important; }
    .tx-row:hover { background: #22252b !important; }
    .stButton > div > button[kind="secondary"]:hover { background: #22252b !important; border-color: #3a3d45 !important; }
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
html, body, .stApp { background: var(--bg) !important; }

/* ── Sidebar (sempre dark) ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1421 0%, #131c2e 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"], section[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }
.sb-top { text-align: center; padding: 1.75rem 1rem 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 0.5rem; }
.sb-top .logo { width: 40px; height: 40px; background: linear-gradient(135deg, #1a56db, #2563eb); border-radius: 12px; display: inline-flex; align-items: center; justify-content: center; font-size: 1.3rem; margin-bottom: 0.6rem; box-shadow: 0 4px 12px rgba(26,86,219,0.3); }
.sb-top h1 { color: #f1f5f9 !important; font-size: 1rem !important; font-weight: 700 !important; letter-spacing: -0.02em; margin: 0 !important; }
.sb-top span { color: #5b6b8c !important; font-size: 0.62rem; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; }
.nav-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em; color: #3b4b6b; text-transform: uppercase; padding: 0 0.75rem; margin: 1.25rem 0 0.25rem 0; }
.nav-line { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 0.4rem 0.75rem; }
section[data-testid="stSidebar"] .stButton > div > button { background: transparent !important; border: none !important; border-left: 3px solid transparent !important; border-radius: 0 !important; padding: 0.45rem 0.75rem !important; font-size: 0.8rem !important; font-weight: 500 !important; color: #8b9abb !important; text-align: left !important; width: 100% !important; box-shadow: none !important; margin: 0 !important; transition: all 0.12s ease !important; }
section[data-testid="stSidebar"] .stButton > div > button:hover { background: rgba(26,86,219,0.08) !important; border-left-color: rgba(26,86,219,0.3) !important; color: #dce3f0 !important; }
section[data-testid="stSidebar"] .stButton > div > button[kind="primary"], section[data-testid="stSidebar"] .stButton > div > button[data-testid="stBaseButton-primary"] { background: rgba(26,86,219,0.12) !important; border-left-color: #1a56db !important; color: #ffffff !important; font-weight: 600 !important; }
section[data-testid="stSidebar"] .stButton > div > button[kind="primary"]:hover { background: rgba(26,86,219,0.18) !important; }
.sb-foot { position: absolute; bottom: 0.75rem; left: 0.75rem; right: 0.75rem; padding: 0.75rem; border-top: 1px solid rgba(255,255,255,0.04); text-align: center; }
.sb-foot p { font-size: 0.6rem !important; color: #3b4b6b !important; margin: 0 !important; }

/* ── Page header ── */
.pg-hdr { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid var(--border-2); }
.pg-hdr h1 { font-size: 1.4rem !important; font-weight: 700 !important; letter-spacing: -0.03em; color: var(--text) !important; margin: 0 !important; line-height: 1.3; }
.pg-hdr p { color: var(--text-3) !important; font-size: 0.82rem; margin: 0.15rem 0 0 0; }

/* ── KPI ── */
.kpi { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-xl, 16px); padding: 1.1rem 1.25rem; box-shadow: var(--shadow); transition: all 0.2s ease; }
.kpi:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
.kpi .k-label { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-3); margin-bottom: 0.3rem; }
.kpi .k-value { font-family: 'JetBrains Mono', monospace; font-size: 1.35rem; font-weight: 600; color: var(--text); letter-spacing: -0.03em; line-height: 1.2; }
.kpi .k-foot { font-size: 0.68rem; font-weight: 600; margin-top: 0.4rem; display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.1rem 0.5rem; border-radius: 100px; }
.kpi .k-foot.up  { background: var(--green-bg); color: var(--green-2); border: 1px solid var(--green-br); }
.kpi .k-foot.down{ background: var(--red-bg);   color: var(--red-2);   border: 1px solid var(--red-br); }
.kpi .k-foot.neut{ background: var(--brand-bg); color: var(--brand-2); border: 1px solid var(--brand-br); }

/* ── Panel ── */
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.25rem 1.5rem; box-shadow: var(--shadow); margin-bottom: 1rem; }
.panel-hdr { display: flex; align-items: center; gap: 0.5rem; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-3); margin-bottom: 1rem; padding-bottom: 0.65rem; border-bottom: 1.5px solid var(--border-2); }
.panel-hdr .ico { width: 22px; height: 22px; background: var(--brand-bg); border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.7rem; color: var(--brand); flex-shrink: 0; }

/* ── Tags ── */
.tag { display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.2rem 0.55rem; border-radius: 100px; font-size: 0.68rem; font-weight: 600; white-space: nowrap; }
.tag.in  { background: var(--green-bg); color: var(--green-2); border: 1px solid var(--green-br); }
.tag.out { background: var(--red-bg);   color: var(--red-2);   border: 1px solid var(--red-br); }

/* ── Row ── */
.tx-row { display: flex; justify-content: space-between; align-items: center; padding: 0.55rem 0.4rem; border-bottom: 1px solid var(--border-2); transition: 0.2s ease; border-radius: 4px; margin: 0 -0.4rem; }
.tx-row:hover { background: var(--surface-2); padding-left: 0.75rem; }
.tx-row:last-child { border-bottom: none; }
.tx-row .i .desc { font-weight: 600; font-size: 0.82rem; color: var(--text); margin-bottom: 0.1rem; }
.tx-row .i .meta { font-size: 0.68rem; color: var(--text-3); }
.tx-row .a { text-align: right; font-family: 'JetBrains Mono', monospace; flex-shrink: 0; }
.tx-row .a .v { font-weight: 600; font-size: 0.85rem; }
.tx-row .a .t { margin-top: 0.15rem; }

/* ── Goal card ── */
.g-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 0; margin-bottom: 0.85rem; box-shadow: var(--shadow); transition: all 0.2s ease; overflow: hidden; display: flex; }
.g-card:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
.g-card .g-bar { width: 5px; flex-shrink: 0; }
.g-card .g-body { flex: 1; padding: 1.1rem 1.35rem; }
.g-card .hdr { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; gap: 0.5rem; }
.g-card .hdr .nm { font-weight: 700; font-size: 0.88rem; color: var(--text); display: flex; align-items: center; gap: 0.4rem; }
.g-card .hdr .pc { font-weight: 600; font-size: 0.72rem; padding: 0.22rem 0.7rem; border-radius: 100px; white-space: nowrap; }
.g-card .hdr .pc.done { background: var(--green-bg); color: var(--green-2); border: 1px solid var(--green-br); }
.g-card .hdr .pc.go  { background: var(--brand-bg); color: var(--brand-2); border: 1px solid var(--brand-br); }
.g-card .hdr .pc.warn { background: var(--amber-bg); color: var(--amber-2); border: 1px solid var(--amber-br); }
.g-card .hdr .pc.over { background: var(--red-bg); color: var(--red-2); border: 1px solid var(--red-br); }
.g-card .vals { font-size: 0.8rem; color: var(--text-2); font-family: 'JetBrains Mono', monospace; display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.55rem; }
.g-card .vals .cur { font-weight: 600; color: var(--text); }
.g-card .vals .tgt { font-size: 0.72rem; color: var(--text-3); }
.g-card .due { font-size: 0.7rem; color: var(--text-3); margin-top: 0.55rem; display: flex; align-items: center; gap: 0.35rem; }
.g-card .g-track { height: 8px; background: var(--border); border-radius: 100px; overflow: hidden; }
.g-card .g-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width 0.5s ease; }
.g-card.done .g-bar { background: var(--green-2); }
.g-card.done .g-fill { background: linear-gradient(90deg, var(--green-2), #22c55e); }
.g-card.go .g-bar { background: var(--brand-2); }

/* ── Empty ── */
.empty { text-align: center; padding: 2.5rem 1.5rem; border: 1.5px dashed var(--border); border-radius: 16px; background: var(--surface); }
.empty .ic { font-size: 2.2rem; margin-bottom: 0.5rem; opacity: 0.3; }
.empty p { font-size: 0.85rem; font-weight: 600; color: var(--text-2); margin: 0; }
.empty .sb { font-size: 0.75rem; color: var(--text-3); margin-top: 0.25rem; }

/* ── Inputs ── */
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input, .stDateInput > div > div > input, .stSelectbox > div > div > div { border-radius: 8px !important; border: 1.5px solid var(--border) !important; background: var(--surface) !important; font-size: 0.82rem !important; transition: all 0.15s ease !important; color: var(--text) !important; caret-color: var(--brand) !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus, .stNumberInput > div > div > input:focus, .stDateInput > div > div > input:focus { border-color: var(--brand) !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important; }
.stSelectbox > div > div > div:focus-within { border-color: var(--brand) !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important; }
div[data-baseweb="select"] > div { border-radius: 8px !important; border: 1.5px solid var(--border) !important; font-size: 0.82rem !important; }
.stSelectbox label, .stNumberInput label, .stDateInput label, .stTextInput label { font-weight: 600 !important; font-size: 0.78rem !important; color: var(--text-2) !important; }
.stSelectbox div[data-baseweb="select"] span, .stSelectbox div[role="combobox"] { color: var(--text) !important; }

.stButton > div > button { border-radius: 8px !important; font-weight: 600 !important; font-size: 0.8rem !important; padding: 0.45rem 1.1rem !important; transition: all 0.15s ease !important; }
.stButton > div > button[kind="primary"] { background: linear-gradient(135deg, #1a56db, #2563eb) !important; border: none !important; color: #fff !important; box-shadow: 0 2px 8px rgba(26,86,219,0.25) !important; }
.stButton > div > button[kind="primary"]:hover { box-shadow: 0 4px 14px rgba(26,86,219,0.4) !important; transform: translateY(-1px) !important; }
.stButton > div > button[kind="secondary"] { background: var(--surface) !important; border: 1.5px solid var(--border) !important; color: var(--text-2) !important; }
.stButton > div > button[kind="secondary"]:hover { background: var(--surface-2) !important; border-color: var(--text-3) !important; }

.stProgress > div > div { background: var(--border-2) !important; border-radius: 100px !important; height: 6px !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, var(--brand), var(--brand-2)) !important; border-radius: 100px !important; }

.stDataFrame { border-radius: 8px !important; overflow: hidden !important; border: 1px solid var(--border) !important; }
.stForm { border: none !important; background: transparent !important; padding: 0 !important; }
.stAlert { border-radius: 10px !important; }

/* Streamlit dark mode overrides via attribute */
[data-theme="dark"] {
    --bg:        #0f1115;
    --surface:   #1a1d23;
    --surface-2: #22252b;
    --border:    #2e3038;
    --border-2:  #26282f;
    --text:      #e8eaed;
    --text-2:    #b0b3b8;
    --text-3:    #72757a;
    --brand:     #3b82f6;
    --brand-2:   #60a5fa;
    --brand-bg:  #1e2433;
    --brand-br:  #2e3a5c;
    --green:     #34d399;
    --green-2:   #6ee7b7;
    --green-bg:  #14291e;
    --green-br:  #1f3d2e;
    --red:       #f87171;
    --red-2:     #fca5a5;
    --red-bg:    #2d1414;
    --red-br:    #4a2020;
    --amber:     #fbbf24;
    --amber-bg:  #2d2410;
    --amber-br:  #4a3a1a;
    --shadow:    0 1px 4px rgba(0,0,0,0.25);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.35);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.45);
}
[data-theme="dark"] .stApp header { background: #0f1115 !important; }
[data-theme="dark"] section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080b12 0%, #0e111a 100%) !important;
}
[data-theme="dark"] section[data-testid="stSidebar"] .stButton > div > button:hover { color: #e0e3e8 !important; }
[data-theme="dark"] .tx-row:hover { background: #22252b !important; }
[data-theme="dark"] .stButton > div > button[kind="secondary"]:hover { background: #22252b !important; border-color: #3a3d45 !important; }

@media (max-width: 768px) {
    .kpi .k-value { font-size: 1.1rem !important; }
    .pg-hdr h1 { font-size: 1.15rem !important; }
}
</style>
""", unsafe_allow_html=True)

def api(metodo, aba, dados=None, valores=None):
    try:
        params = {"acao": metodo, "aba": aba}
        if metodo == "put":
            r = _http.post(API_URL, json={"aba": aba, "id": dados, "valores": valores, "acao": "put"}, timeout=30)
        elif metodo == "delete":
            r = _http.post(API_URL, json={"aba": aba, "id": dados, "acao": "delete"}, timeout=30)
        elif metodo == "post":
            r = _http.post(API_URL, json={"aba": aba, "valores": dados}, timeout=30)
        else:
            r = _http.get(API_URL, params=params, timeout=30)
        if r.status_code == 200:
            j = r.json()
            if isinstance(j, dict) and j.get("_httpCode", 200) >= 400:
                st.error(f"Servidor: {j.get('erro', 'erro desconhecido')}")
                return None
            return j
        try:
            t = r.text[:300]
            st.error(f"HTTP {r.status_code}: {t}")
        except Exception:
            st.error(f"HTTP {r.status_code}")
        return None
    except requests.Timeout:
        st.error("Tempo limite excedido. Verifique o Web App.")
    except requests.ConnectionError:
        st.error("Falha de conexao. Verifique a URL.")
    except Exception as e:
        st.error(f"Erro: {e}")
    return None

def ler(aba):
    d = api("ler", aba)
    return pd.DataFrame(d) if d and isinstance(d, list) else pd.DataFrame()

def escrever(aba, valores):
    return api("post", aba, valores)

def excluir(aba, id_registro):
    return api("delete", aba, id_registro)

def atualizar(aba, id_registro, valores):
    return api("put", aba, id_registro, valores)

def prox_id(df):
    if df.empty:
        return "1"
    ids = pd.to_numeric(df["ID"], errors="coerce").fillna(0).astype(int)
    return str(ids.max() + 1)

def sn(v):
    return pd.to_numeric(v, errors="coerce").fillna(0)

def preparar_df(df):
    if df.empty:
        return df
    df = df.copy()
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=False)
    if "Valor" in df.columns:
        df["Valor"] = sn(df["Valor"])
    if "Data" in df.columns and not df["Data"].isna().all():
        df = df.dropna(subset=["Data"])
        df["Mes"] = df["Data"].dt.month
        df["Ano"] = df["Data"].dt.year
        df["MesAno"] = df["Data"].dt.to_period("M").astype(str)
    return df

def auto_gerar_fixos():
    now = datetime.now()
    mes_atual = now.month
    ano_atual = now.year
    df = ler("Transacoes")
    if df.empty or "Fixo" not in df.columns:
        return 0

    df = preparar_df(df)
    fixos = df[(df["Fixo"] == "Sim") & (df["Tipo"] == "Despesa")]
    if fixos.empty:
        return 0

    fixos_unicos = fixos.drop_duplicates(subset=["Descricao", "Categoria", "Responsavel", "Valor", "Parcelas", "Tipo"])
    criadas = 0
    df_t = ler("Transacoes")
    df_t = preparar_df(df_t)

    for _, f in fixos_unicos.iterrows():
        existe = df_t[
            (df_t["Data"].dt.month == mes_atual) &
            (df_t["Data"].dt.year == ano_atual) &
            (df_t["Descricao"] == f["Descricao"]) &
            (df_t["Categoria"] == f["Categoria"]) &
            (df_t["Responsavel"] == f["Responsavel"]) &
            (df_t["Valor"] == f["Valor"])
        ]
        if existe.empty:
            dia = min(f["Data"].day if pd.notna(f["Data"]) else now.day, 28)
            try:
                dt = date(ano_atual, mes_atual, dia)
            except ValueError:
                dt = date(ano_atual, mes_atual, 1)
            res = escrever("Transacoes", [
                prox_id(df_t), dt.strftime("%Y-%m-%d"),
                f["Tipo"], f["Categoria"], f["Descricao"],
                str(f["Valor"]), str(f["Parcelas"]), f["Responsavel"], "Sim"
            ])
            if res and res.get("status") == "ok":
                criadas += 1

    if criadas > 0:
        st.info(f"🔁 {criadas} gasto(s) fixo(s) registrado(s) automaticamente neste mes.")
    return criadas

def kpi(label, value, footer="", kind="neut"):
    f = f'<span class="k-foot {kind}">{footer}</span>' if footer else ""
    return f'<div class="kpi"><div class="k-label">{label}</div><div class="k-value">{value}</div>{f}</div>'

def panel(title, icon):
    st.markdown(f'<div class="panel"><div class="panel-hdr"><span class="ico">{icon}</span> {title}</div>', unsafe_allow_html=True)
    return st.container()

def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)

def hdr(title, subtitle=""):
    st.markdown(f'<div class="pg-hdr"><h1>{title}</h1>{f"<p>{subtitle}</p>" if subtitle else ""}</div>', unsafe_allow_html=True)

def nav_btn(label, icon, active):
    return st.sidebar.button(f"{icon}  {label}", key=f"n_{label.replace(' ','')}", type="primary" if active else "secondary", use_container_width=True)

def sidebar():
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    with st.sidebar:
        st.markdown("""
        <div class="sb-top">
            <div class="logo">💰</div>
            <h1>Financas do Casal</h1>
            <span>Controle financeiro em dupla</span>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="nav-label">Principal</div>', unsafe_allow_html=True)
        if nav_btn("Dashboard", "🏠", st.session_state.page == "Dashboard"):
            st.session_state.page = "Dashboard"; st.rerun()
        if nav_btn("Relatorios", "📊", st.session_state.page == "Relatorios"):
            st.session_state.page = "Relatorios"; st.rerun()
        st.markdown('<hr class="nav-line">', unsafe_allow_html=True)
        st.markdown('<div class="nav-label">Gerenciamento</div>', unsafe_allow_html=True)
        if nav_btn("Nova Transacao", "➕", st.session_state.page == "Nova Transacao"):
            st.session_state.page = "Nova Transacao"; st.rerun()
        if nav_btn("Transacoes", "📋", st.session_state.page == "Transacoes"):
            st.session_state.page = "Transacoes"; st.rerun()
        if nav_btn("Metas", "🎯", st.session_state.page == "Metas"):
            st.session_state.page = "Metas"; st.rerun()
        if nav_btn("Categorias", "📁", st.session_state.page == "Categorias"):
            st.session_state.page = "Categorias"; st.rerun()
        st.markdown('<hr class="nav-line">', unsafe_allow_html=True)
        st.markdown('<div class="nav-label">Suporte</div>', unsafe_allow_html=True)
        if nav_btn("Manual", "📖", st.session_state.page == "Manual"):
            st.session_state.page = "Manual"; st.rerun()
        st.markdown('<div class="sb-foot"><p>financasdocal.com.br</p></div>', unsafe_allow_html=True)
        return st.session_state.page

def page_dashboard():
    auto_gerar_fixos()

    df = ler("Transacoes")
    now = datetime.now()

    hdr("Dashboard", "Visao geral das suas financas")

    c1, c2 = st.columns(2)
    with c1:
        mes = st.selectbox("Mes", range(1, 13), index=now.month - 1, format_func=lambda x: MESES[x-1], key="d_mes")
    with c2:
        ano = st.selectbox("Ano", range(2024, 2031), index=now.year - 2024, key="d_ano")

    df = preparar_df(df)
    dm = df[(df["Mes"] == mes) & (df["Ano"] == ano)] if not df.empty else pd.DataFrame()
    receitas = dm[dm["Tipo"] == "Receita"]["Valor"].sum() if not dm.empty else 0
    despesas = dm[dm["Tipo"] == "Despesa"]["Valor"].sum() if not dm.empty else 0
    saldo = receitas - despesas
    fixos = dm[(dm["Tipo"] == "Despesa") & (dm.get("Fixo", "Nao") == "Sim")]["Valor"].sum() if not dm.empty else 0
    variaveis = despesas - fixos

    st.markdown(f"""
    <div style="display:flex; gap:0.75rem; margin-bottom:1rem; flex-wrap:wrap;">
        {kpi("Receitas", f"R$ {receitas:,.2f}", f"▲ {MESES[mes-1]}", "up")}
        {kpi("Despesas", f"R$ {despesas:,.2f}", f"▼ {MESES[mes-1]}", "down")}
        {kpi("Gastos Fixos", f"R$ {fixos:,.2f}", f"{(fixos/despesas*100):.0f}%" if despesas > 0 else "", "neut")}
        {kpi("Saldo", f"R$ {saldo:,.2f}", "▲ Positivo" if saldo >= 0 else "▼ Negativo", "up" if saldo >= 0 else "down")}
    </div>
    """, unsafe_allow_html=True)

    if dm.empty:
        st.markdown('<div class="empty"><div class="ic">📊</div><p>Nenhuma transacao neste periodo</p><div class="sb">Cadastre transacoes em "Nova Transacao"</div></div>', unsafe_allow_html=True)
        return

    e1, e2 = st.columns([5, 4])
    with e1:
        g1, g2 = st.columns(2)
        with g1:
            with panel("Despesas por Categoria", "🏷️"):
                dc = dm[dm["Tipo"] == "Despesa"].groupby("Categoria")["Valor"].sum().sort_values(ascending=True)
                if not dc.empty:
                    st.bar_chart(dc, height=170, color="#dc2626")
                else:
                    st.markdown('<div class="empty"><p>Sem despesas</p></div>', unsafe_allow_html=True)
            panel_end()
        with g2:
            with panel("Fixos vs Variaveis", "🔁"):
                if despesas > 0:
                    fv = pd.DataFrame({"Tipo": ["Fixos", "Variaveis"], "Valor": [fixos, variaveis]}).set_index("Tipo")
                    st.bar_chart(fv, height=170, color=["#1a56db", "#dc2626"])
                else:
                    st.markdown('<div class="empty"><p>Sem despesas</p></div>', unsafe_allow_html=True)
            panel_end()
    with e2:
        with panel("Ultimas Transacoes", "🕐"):
            ult = dm.sort_values("Data", ascending=False).head(7)
            for _, r in ult.iterrows():
                tc = "in" if r["Tipo"] == "Receita" else "out"
                sv = "+" if r["Tipo"] == "Receita" else "-"
                cr = "#059669" if r["Tipo"] == "Receita" else "#dc2626"
                dt = str(r["Data"])[:10] if pd.notna(r["Data"]) else ""
                st.markdown(f"""
                <div class="tx-row">
                    <div class="i"><div class="desc">{r['Descricao']}</div><div class="meta">{r['Responsavel']} &middot; {r['Categoria']} &middot; {dt}</div></div>
                    <div class="a"><div class="v" style="color:{cr};">{sv} R$ {r['Valor']:,.2f}</div><span class="tag {tc}">{r['Tipo']}</span></div>
                </div>""", unsafe_allow_html=True)
        panel_end()

def page_nova():
    hdr("Nova Transacao", "Registre receitas e despesas")
    with st.form("fn", clear_on_submit=True):
        with panel("Dados da Transacao", "📝"):
            cats = ler("Categorias")
            c1, c2 = st.columns(2)
            data = c1.date_input("Data", value=date.today())
            tipo = c2.selectbox("Tipo", ["Receita", "Despesa"])
            cl = cats[cats["Tipo"] == tipo]["Nome"].tolist() if not cats.empty else ["Geral"]
            if not cl: cl = ["Geral"]
            c3, c4 = st.columns(2)
            categoria = c3.selectbox("Categoria", cl)
            parcelas = c4.number_input("Parcelas", min_value=1, max_value=48, value=1)
            desc = st.text_input("Descricao", placeholder="Ex: Supermercado, Freelance...")
            c5, c6 = st.columns(2)
            valor = c5.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f")
            resp = c6.text_input("Responsavel", placeholder="Quem pagou?")
            c7, c8 = st.columns(2)
            fixo = c7.checkbox("🔁 Despesa Fixa (recorrente)", value=False, help="Marque para gastos que se repetem todo mes como aluguel, assinaturas, etc.")
            st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)
            if st.form_submit_button("Salvar Transacao", type="primary", use_container_width=True):
                erros = []
                if not desc: erros.append("descricao")
                if not resp: erros.append("responsavel")
                if valor <= 0: erros.append("valor valido")
                if erros:
                    st.warning(f"Informe: {', '.join(erros)}")
                else:
                    df_t = ler("Transacoes")
                    fixo_val = "Sim" if fixo else "Nao"
                    res = escrever("Transacoes", [prox_id(df_t), data.strftime("%Y-%m-%d"), tipo, categoria, desc, str(valor), str(parcelas), resp, fixo_val])
                    if res and res.get("status") == "ok":
                        st.success("Transacao salva!")
                        st.rerun()
                    else:
                        st.error("Erro ao salvar")
        panel_end()

def page_transacoes():
    hdr("Transacoes", "Visualize, filtre e gerencie seus registros")
    df = ler("Transacoes")
    if df.empty:
        st.markdown('<div class="empty"><div class="ic">📋</div><p>Nenhuma transacao cadastrada</p><div class="sb">Va em "Nova Transacao" para comecar</div></div>', unsafe_allow_html=True)
        return
    df = preparar_df(df)

    tem_fixo = "Fixo" in df.columns

    with panel("Filtros", "🔍"):
        cols = 5 if tem_fixo else 4
        cols_list = st.columns(cols)
        tf = cols_list[0].selectbox("Tipo", ["Todos", "Receita", "Despesa"])
        cf = cols_list[1].selectbox("Categoria", ["Todas"] + sorted(df["Categoria"].dropna().unique()))
        rf = cols_list[2].selectbox("Responsavel", ["Todos"] + sorted(df["Responsavel"].dropna().unique()))
        if tem_fixo:
            ff = cols_list[3].selectbox("Fixo", ["Todos", "Sim", "Nao"])
        else:
            ff = "Todos"
        bs = cols_list[-1].text_input("Buscar", placeholder="Descricao...")
    panel_end()

    flt = df.copy()
    if tf != "Todos": flt = flt[flt["Tipo"] == tf]
    if cf != "Todas": flt = flt[flt["Categoria"] == cf]
    if rf != "Todos": flt = flt[flt["Responsavel"] == rf]
    if ff != "Todos" and tem_fixo: flt = flt[flt["Fixo"] == ff]
    if bs: flt = flt[flt["Descricao"].str.contains(bs, case=False, na=False)]

    rec = flt[flt["Tipo"] == "Receita"]["Valor"].sum()
    desp = flt[flt["Tipo"] == "Despesa"]["Valor"].sum()
    sal = rec - desp
    qtd_fixos = len(flt[(flt.get("Fixo", "Nao") == "Sim") & (flt["Tipo"] == "Despesa")]) if tem_fixo else 0

    st.markdown(f"""
    <div style="display:flex; gap:0.75rem; margin-bottom:1rem;">
        {kpi("Registros", str(len(flt)), kind="neut")}
        {kpi("Receitas", f"R$ {rec:,.2f}", kind="up")}
        {kpi("Despesas", f"R$ {desp:,.2f}", kind="down")}
        {kpi("Saldo", f"R$ {sal:,.2f}", kind="up" if sal >= 0 else "down")}
        {kpi("Fixos", str(qtd_fixos), kind="neut") if tem_fixo else ""}
    </div>
    """, unsafe_allow_html=True)

    with panel(f"Registros ({len(flt)})", "📄"):
        cols_df = ["ID","Data","Tipo","Categoria","Descricao","Valor","Parcelas","Responsavel"]
        if tem_fixo:
            cols_df.append("Fixo")
        st.dataframe(
            flt.sort_values("Data", ascending=False)[cols_df].reset_index(drop=True),
            use_container_width=True, hide_index=True, height=min(len(flt)*38+60, 420))
    panel_end()

    with panel("Excluir Registro", "🗑️"):
        c1, c2 = st.columns([4, 1])
        idx = c1.text_input("ID", placeholder="Digite o ID...", label_visibility="collapsed")
        if c2.button("Excluir", type="secondary", use_container_width=True):
            if not idx:
                st.warning("Informe o ID")
            else:
                res = excluir("Transacoes", idx)
                if res and res.get("status") == "ok":
                    st.success("Registro excluido!"); st.rerun()
                else:
                    st.error("ID nao encontrado")
    panel_end()

def page_relatorios():
    hdr("Relatorios", "Analise detalhada das suas financas")
    df = ler("Transacoes")
    if df.empty:
        st.markdown('<div class="empty"><div class="ic">📊</div><p>Sem dados para gerar relatorios</p><div class="sb">Cadastre transacoes primeiro</div></div>', unsafe_allow_html=True)
        return
    df = preparar_df(df)
    if df.empty:
        st.markdown('<div class="empty"><div class="ic">📊</div><p>Nao ha dados com datas validas</p></div>', unsafe_allow_html=True)
        return

    with panel("Resumo Mensal", "📅"):
        r = df.groupby(["MesAno", "Tipo"])["Valor"].sum().unstack(fill_value=0)
        if "Receita" in r.columns and "Despesa" in r.columns:
            r["Saldo"] = r["Receita"] - r["Despesa"]
            r["Economia"] = r["Saldo"] / r["Receita"] * 100
            r["Economia"] = r["Economia"].round(1).astype(str) + "%"
        st.dataframe(r, use_container_width=True)
    panel_end()

    c1, c2 = st.columns(2)
    with c1:
        with panel("Despesas por Categoria", "🏷️"):
            dc = df[df["Tipo"] == "Despesa"].groupby("Categoria")["Valor"].sum().sort_values(ascending=True)
            if not dc.empty:
                st.bar_chart(dc, height=260, color="#dc2626")
            else:
                st.markdown('<div class="empty"><p>Nenhuma despesa</p></div>', unsafe_allow_html=True)
        panel_end()
    with c2:
        with panel("Por Responsavel", "👥"):
            pp = df.groupby(["Responsavel", "Tipo"])["Valor"].sum().unstack(fill_value=0)
            if not pp.empty:
                st.dataframe(pp, use_container_width=True)
                st.bar_chart(pp, height=160, color=["#1a56db", "#dc2626"])
            else:
                st.markdown('<div class="empty"><p>Sem dados</p></div>', unsafe_allow_html=True)
        panel_end()

    with panel("Evolucao Mensal", "📈"):
        ev = df.groupby("MesAno")["Valor"].sum()
        if not ev.empty:
            st.area_chart(ev, height=240, color="#1a56db")
    panel_end()

def page_metas():
    hdr("Metas Financeiras", "Defina objetivos e acompanhe o progresso")
    df = ler("Metas")

    with st.form("fm", clear_on_submit=True):
        with panel("Nova Meta", "🎯"):
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome", placeholder="Ex: Reserva de Emergencia...")
            va = c2.number_input("Valor Alvo (R$)", min_value=1.0, step=100.0, format="%.2f")
            prazo = c1.date_input("Prazo", value=date.today())
            vat = c2.number_input("Valor Atual (R$)", min_value=0.0, step=10.0, format="%.2f")
            if st.form_submit_button("Criar Meta", type="primary", use_container_width=True):
                if nome and va > 0:
                    res = escrever("Metas", [prox_id(df), nome, str(va), str(vat), prazo.strftime("%Y-%m-%d")])
                    if res and res.get("status") == "ok":
                        st.success("Meta criada!"); st.rerun()
                    else:
                        st.error("Erro ao salvar")
        panel_end()

    if df.empty:
        st.markdown('<div class="empty"><div class="ic">🎯</div><p>Nenhuma meta cadastrada</p><div class="sb">Defina um objetivo acima para comecar</div></div>', unsafe_allow_html=True)
        return

    df["ValorAlvo"] = sn(df["ValorAlvo"])
    df["ValorAtual"] = sn(df["ValorAtual"])
    df["Prazo"] = pd.to_datetime(df.get("Prazo"), errors="coerce")

    talvo = df["ValorAlvo"].sum()
    tatual = df["ValorAtual"].sum()
    pctg = min(tatual / talvo, 1.0) * 100 if talvo > 0 else 0
    conc = len(df[df["ValorAtual"] >= df["ValorAlvo"]])
    pend = len(df[df["ValorAtual"] < df["ValorAlvo"]])

    st.markdown(f"""
    <div style="display:flex; gap:0.75rem; margin:1rem 0;">
        {kpi("Total em Metas", f"R$ {talvo:,.2f}", kind="neut")}
        {kpi("Total Acumulado", f"R$ {tatual:,.2f}", kind="up")}
        {kpi("Progresso Geral", f"{pctg:.0f}%", f"{conc} concluidas", "up" if conc == len(df) else "neut")}
        {kpi("Pendentes", str(pend), "metas em andamento", "down" if pend else "neut")}
    </div>
    """, unsafe_allow_html=True)

    hoje = date.today()
    card_ativo = lambda m: m["ValorAtual"] < m["ValorAlvo"]
    ativas = df[df.apply(card_ativo, axis=1)].sort_values("ValorAtual", ascending=False)
    feitas = df[~df.apply(card_ativo, axis=1)].sort_values("ValorAlvo", ascending=False)

    def render_meta(m):
        pct = min(m["ValorAtual"] / m["ValorAlvo"], 1.0) * 100 if m["ValorAlvo"] > 0 else 0
        feito = pct >= 100
        cls = "done" if feito else "go"
        ic = "✅" if feito else "🎯"

        prazo_info = ""
        if pd.notna(m["Prazo"]):
            pdt = m["Prazo"].date()
            dias = (pdt - hoje).days
            if feito:
                chip = '<span class="pc done">Concluida</span>'
            elif dias < 0:
                chip = f'<span class="pc over">Prazo vencido ha {-dias}d</span>'
                cls = "go"
            elif dias <= 30:
                chip = f'<span class="pc warn">Faltam {dias}d</span>'
            else:
                chip = f'<span class="pc go">Faltam {dias}d</span>'
            meses = max((dias // 30) + 1, 1) if dias > 0 else None
            taxa = (m["ValorAlvo"] - m["ValorAtual"]) / meses if meses else 0
            prazo_info = f'<div class="due">📅 {pdt.strftime("%d/%m/%Y")}'
            if not feito and taxa > 0:
                prazo_info += f' &middot; Guardar <strong>R$ {taxa:,.2f}/mes</strong>'
            prazo_info += '</div>'
        elif not feito:
            chip = f'<span class="pc go">{pct:.0f}%</span>'
        else:
            chip = '<span class="pc done">Concluida</span>'

        st.markdown(f"""
        <div class="g-card {cls}">
            <div class="g-bar"></div>
            <div class="g-body">
                <div class="hdr"><span class="nm">{ic} {m["Nome"]}</span>{chip}</div>
                <div class="vals"><span class="cur">R$ {m["ValorAtual"]:,.2f}</span><span class="tgt">de R$ {m["ValorAlvo"]:,.2f} &middot; {pct:.0f}%</span></div>
                <div class="g-track"><div class="g-fill" style="width:{pct:.0f}%"></div></div>
                {prazo_info}
            </div>
        </div>""", unsafe_allow_html=True)

        a1, a2, a3 = st.columns([3, 1, 1])
        novo = a1.number_input("Adicionar valor", min_value=0.0, step=50.0, format="%.2f", key=f"mv_{m['ID']}", label_visibility="collapsed", placeholder="Adicionar R$...")
        if a2.button("➕", key=f"mb_{m['ID']}", use_container_width=True, help="Adicionar valor"):
            if novo > 0:
                novo_atual = m["ValorAtual"] + novo
                res = atualizar("Metas", m["ID"], [m["ID"], m["Nome"], str(m["ValorAlvo"]), str(novo_atual), m["Prazo"].strftime("%Y-%m-%d") if pd.notna(m["Prazo"]) else ""])
                if res and res.get("status") == "ok":
                    st.success("Valor adicionado!"); st.rerun()
                else:
                    st.error("Erro ao atualizar")
        if a3.button("🗑️", key=f"gd_{m['ID']}", use_container_width=True, help="Excluir meta"):
            res = excluir("Metas", m["ID"])
            if res and res.get("status") == "ok":
                st.success("Meta excluida!"); st.rerun()
            else:
                st.error("Erro ao excluir")

    with panel(f"Em Andamento ({len(ativas)})", "🚀"):
        if not ativas.empty:
            for _, m in ativas.iterrows():
                render_meta(m)
        else:
            st.markdown('<div class="empty"><p>Nenhuma meta em andamento</p></div>', unsafe_allow_html=True)
    panel_end()

    with panel(f"Concluidas ({len(feitas)})", "✅"):
        if not feitas.empty:
            for _, m in feitas.iterrows():
                render_meta(m)
        else:
            st.markdown('<div class="empty"><p>Nenhuma meta concluida ainda</p></div>', unsafe_allow_html=True)
    panel_end()

def page_categorias():
    hdr("Categorias", "Gerencie as categorias de receitas e despesas")
    df = ler("Categorias")

    if not df.empty and "Tipo" in df.columns:
        rc = len(df[df["Tipo"] == "Receita"])
        dc = len(df[df["Tipo"] == "Despesa"])
        st.markdown(f"""
        <div style="display:flex; gap:0.75rem; margin-bottom:1rem;">
            {kpi("Total", str(len(df)), kind="neut")}
            {kpi("Receitas", str(rc), kind="up")}
            {kpi("Despesas", str(dc), kind="down")}
        </div>
        """, unsafe_allow_html=True)

        with panel("Categorias Cadastradas", "📂"):
            for _, r in df.iterrows():
                cc = "in" if r.get("Tipo") == "Receita" else "out"
                st.markdown(f'<div class="tx-row"><div class="i"><div class="desc">{r.get("Nome","")}</div></div><span class="tag {cc}">{r.get("Tipo","")}</span></div>', unsafe_allow_html=True)
        panel_end()

    with st.form("fc", clear_on_submit=True):
        with panel("Adicionar Categoria", "➕"):
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome", placeholder="Ex: Gasolina, Mercado...")
            tipo = c2.selectbox("Tipo", ["Receita", "Despesa"])
            if st.form_submit_button("Adicionar", type="primary", use_container_width=True):
                if nome:
                    pid = prox_id(df) if not df.empty else "1"
                    res = escrever("Categorias", [pid, nome, tipo])
                    if res and res.get("status") == "ok":
                        st.success("Categoria adicionada!"); st.rerun()
                    else:
                        st.error("Erro ao adicionar")
        panel_end()

def page_manual():
    hdr("Manual do Usuario", "Guia de configuracao e uso")
    passos = [
        ("1", "Criar Planilha", "Crie uma planilha em branco no Google Sheets e nomeie como <strong>Financas Casal</strong>."),
        ("2", "Executar Apps Script", "Va em <strong>Extensoes → Apps Script</strong>. Cole o codigo de <code>apps_script.js</code>, salve e execute <code>SetupBancoDados</code>. Autorize."),
        ("3", "Implantar Web App", "<strong>Implantar → Nova implantacao</strong> → Aplicativo da web, Executar como: Eu, Acesso: Qualquer pessoa. Copie a URL."),
        ("4", "Configurar .env", "Crie <code>.env</code> com:<br><code>API_URL=https://script.google.com/macros/s/SEU_ID/exec</code>"),
        ("5", "Instalar e Rodar", "Terminal:<br><code>pip install -r requirements.txt</code><br><code>streamlit run app.py</code><br>Acesse <strong>http://localhost:8501</strong>"),
    ]
    for n, t, d in passos:
        st.markdown(f"""
        <div style="display:flex; gap:1rem; align-items:flex-start; background:#fff; border:1px solid var(--border); border-radius:var(--radius-xl); padding:1.1rem 1.35rem; margin-bottom:0.65rem; box-shadow:var(--shadow);">
            <div style="flex-shrink:0; width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg,#1a56db,#2563eb); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.9rem;">{n}</div>
            <div><div style="font-weight:700; color:var(--text); font-size:0.9rem; margin-bottom:0.2rem;">{t}</div><div style="font-size:0.82rem; color:var(--text-2); line-height:1.6;">{d}</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    with panel("Estrutura da Planilha", "📋"):
        st.markdown("""
| **Aba** | **Colunas** |
|---|---|
| **Categorias** | ID, Nome, Tipo |
| **Transacoes** | ID, Data, Tipo, Categoria, Descricao, Valor, Parcelas, Responsavel, Fixo |
| **Metas** | ID, Nome, ValorAlvo, ValorAtual, Prazo |
| **Config** | Chave, Valor |
        """)
    panel_end()

def main():
    if not API_URL:
        st.markdown(f"""
        <div style="text-align:center; padding:4rem 1.5rem;">
            <div style="font-size:3.5rem; margin-bottom:1rem; opacity:0.4;">⚙️</div>
            <h2 style="color:#1a1d21; font-weight:700; font-size:1.3rem; margin-bottom:0.5rem;">Configuracao Necessaria</h2>
            <p style="color:#6b7280; font-size:0.85rem; max-width:420px; margin:0 auto 1.5rem;">Configure a URL do Web App no arquivo <code style="background:#f3f4f6; padding:0.15rem 0.4rem; border-radius:4px;">.env</code></p>
            <div style="background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:1.5rem 2rem; max-width:560px; margin:0 auto; text-align:left; font-size:0.82rem; color:#4b5563; line-height:1.8;">
                <strong style="color:#111827;">Passos:</strong><br>
                1. Crie uma planilha no Google Sheets<br>
                2. Extensoes → Apps Script → cole <code>apps_script.js</code><br>
                3. Execute <code>SetupBancoDados</code> e autorize<br>
                4. Implantar → Nova implantacao → Aplicativo da web<br>
                5. Copie a URL e cole no <code>.env</code><br><br>
                <div style="background:#eef3ff; border:1px solid #c7d7fe; border-radius:8px; padding:0.6rem 1rem;"><code style="font-size:0.75rem;">API_URL=https://script.google.com/macros/s/SEU_ID/exec</code></div>
            </div>
        </div>""", unsafe_allow_html=True)
        return

    pagina = sidebar()
    paginas = {
        "Dashboard": page_dashboard, "Nova Transacao": page_nova,
        "Transacoes": page_transacoes, "Relatorios": page_relatorios,
        "Metas": page_metas, "Categorias": page_categorias, "Manual": page_manual,
    }
    with st.container():
        paginas[pagina]()

if __name__ == "__main__":
    main()
