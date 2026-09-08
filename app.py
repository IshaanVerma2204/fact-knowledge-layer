import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Fact Knowledge Layer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Palette ── */
:root {
  --bg-base:     #11111b;
  --bg-mantle:   #181825;
  --bg-crust:    #1e1e2e;
  --bg-surface0: #313244;
  --bg-surface1: #45475a;
  --text-main:   #cdd6f4;
  --text-muted:  #a6adc8;
  --text-dim:    #6c7086;
  --accent:      #cba6f7;
  --accent-dark: #b48ef0;
  --blue:        #89b4fa;
  --green:       #a6e3a1;
  --red:         #f38ba8;
  --yellow:      #f9e2af;
  --teal:        #94e2d5;
  --peach:       #fab387;
}

/* ── Base ── */
html, body, [class*="css"] {
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
  color: var(--text-main);
  background-color: var(--bg-base);
}
.block-container {
  padding-top: 2.5rem !important;
  padding-bottom: 3rem !important;
  max-width: 1200px;
}

/* ── Keyframes ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0);    }
}
@keyframes shimmer {
  0%   { background-position: -800px 0; }
  100% { background-position:  800px 0; }
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes pulseRing {
  0%, 100% { box-shadow: 0 0 0 0   rgba(203,166,247,.5); }
  50%       { box-shadow: 0 0 0 8px rgba(203,166,247,0);  }
}
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-10px); }
  to   { opacity: 1; transform: translateX(0);     }
}

/* ════════════════════════════════
   SIDEBAR
════════════════════════════════ */
[data-testid="stSidebar"] {
  background: var(--bg-mantle) !important;
  border-right: 1px solid var(--bg-surface0);
}
.sidebar-header {
  padding: 1.25rem 0 .75rem;
  border-bottom: 1px solid var(--bg-surface0);
  margin-bottom: 1.25rem;
}
.sidebar-wordmark {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
  color: var(--accent);
}
.sidebar-wordmark span {
  color: var(--text-muted);
  font-weight: 400;
}
.sidebar-section-label {
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin: 1.25rem 0 .6rem;
}

/* Metric cards */
div[data-testid="stMetric"] {
  background: var(--bg-crust) !important;
  border: 1px solid var(--bg-surface0);
  border-radius: 8px;
  padding: 12px 16px !important;
  transition: border-color .2s ease, box-shadow .2s ease;
}
div[data-testid="stMetric"]:hover {
  border-color: var(--accent);
  box-shadow: 0 0 0 1px rgba(203,166,247,.2);
}
div[data-testid="stMetricValue"] {
  font-size: 1.75rem !important;
  font-weight: 700 !important;
  color: var(--text-main) !important;
  letter-spacing: -.02em;
}
div[data-testid="stMetricLabel"] {
  font-size: .7rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: .08em !important;
  color: var(--text-dim) !important;
}

/* Stat bars */
.stat-bar-wrap { margin: 5px 0 12px; }
.stat-bar-label {
  display: flex; justify-content: space-between;
  font-size: .73rem; color: var(--text-muted); margin-bottom: 5px;
}
.stat-bar-label strong { font-weight: 500; }
.stat-bar {
  height: 4px; background: var(--bg-surface0);
  border-radius: 999px; overflow: hidden;
}
.stat-bar-fill {
  height: 100%; border-radius: 999px;
  transition: width .5s cubic-bezier(.4,0,.2,1);
}

/* Document list */
.doc-entry {
  display: flex; align-items: center; gap: 9px;
  padding: 7px 10px;
  border-radius: 6px;
  border: 1px solid var(--bg-surface0);
  background: var(--bg-crust);
  margin-bottom: 5px;
  animation: fadeUp .3s ease both;
}
.doc-entry .status-dot {
  width: 6px; height: 6px;
  border-radius: 50%; flex-shrink: 0;
}
.doc-entry .doc-name {
  font-size: .78rem; color: var(--text-muted);
  font-weight: 500; flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* ════════════════════════════════
   PAGE HEADER
════════════════════════════════ */
.page-header {
  margin-bottom: 1.75rem;
  animation: fadeUp .6s cubic-bezier(.16,1,.3,1) both;
}
.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: -.03em;
  margin-bottom: .3rem;
  line-height: 1.15;
}
.page-title em {
  font-style: normal;
  background: linear-gradient(135deg, var(--accent) 0%, var(--blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.page-subtitle {
  font-size: .9rem;
  color: var(--text-dim);
  font-weight: 400;
  line-height: 1.5;
}

/* ════════════════════════════════
   TABS  (high-specificity overrides required)
════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--bg-surface0) !important;
  border-radius: 0 !important;
  padding: 0 !important;
  gap: 0 !important;
}
/* Kill every tab's default styling */
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"]:focus,
.stTabs [data-baseweb="tab"]:active {
  background: transparent !important;
  border-radius: 0 !important;
  color: var(--text-dim) !important;
  font-weight: 500 !important;
  font-size: .875rem !important;
  padding: 10px 20px !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  transition: color .15s ease !important;
  letter-spacing: .01em !important;
  font-family: 'Inter', sans-serif !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: var(--text-muted) !important;
}
/* Kill the default red underline marker Streamlit injects */
.stTabs [data-baseweb="tab"] div[data-testid="stMarkdownContainer"],
.stTabs [data-baseweb="tab-highlight"] {
  display: none !important;
}
/* Active tab text color */
.stTabs [data-baseweb="tab"][aria-selected="true"],
.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  background: transparent !important;
  border-bottom: 2px solid var(--accent) !important;
  margin-bottom: -1px !important;
}
/* Nuclear option: override the highlight bar Streamlit renders underneath */
.stTabs [data-baseweb="tab-border"] {
  background-color: var(--bg-surface0) !important;
  height: 1px !important;
}
.stTabs [data-baseweb="tab-highlight"] {
  background-color: var(--accent) !important;
  height: 2px !important;
}
.stTabs [data-baseweb="tab-panel"] {
  animation: fadeUp .4s cubic-bezier(.16,1,.3,1) both;
  padding-top: 1.5rem !important;
}


/* ════════════════════════════════
   SECTION HEADINGS
════════════════════════════════ */
.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  letter-spacing: -.01em;
  margin-bottom: 1rem;
}
.section-meta {
  font-size: .8rem;
  color: var(--text-dim);
  margin-bottom: 1rem;
}

/* ════════════════════════════════
   FILE UPLOADER
════════════════════════════════ */
/* Outer wrapper */
[data-testid="stFileUploader"] {
  padding: 0 !important;
}
/* The actual dropzone section */
[data-testid="stFileUploader"] section {
  background: var(--bg-mantle) !important;
  border: 1px dashed var(--bg-surface0) !important;
  border-radius: 10px !important;
  padding: 1.75rem 2rem !important;
  transition: border-color .2s ease, background .2s ease !important;
}
[data-testid="stFileUploader"] section:hover {
  border-color: rgba(203,166,247,.5) !important;
  background: rgba(203,166,247,.03) !important;
}
/* Upload button inside dropzone */
[data-testid="stFileUploader"] section button {
  background: var(--bg-crust) !important;
  border: 1px solid var(--bg-surface0) !important;
  color: var(--text-muted) !important;
  border-radius: 6px !important;
  font-size: .8rem !important;
  font-weight: 500 !important;
}
/* Uploader label text */
[data-testid="stFileUploaderDropzoneInstructions"] {
  color: var(--text-dim) !important;
  font-size: .85rem !important;
}
/* File list items after upload */
[data-testid="stFileUploaderFile"] {
  background: var(--bg-crust) !important;
  border: 1px solid var(--bg-surface0) !important;
  border-radius: 6px !important;
  font-size: .8rem !important;
  color: var(--text-muted) !important;
}

/* File status rows */
.file-status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 1rem 0;
}
.file-status-block { }
.file-status-label {
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--text-dim);
  margin-bottom: 6px;
}
.file-tag {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 10px;
  border-radius: 5px;
  border: 1px solid var(--bg-surface0);
  background: var(--bg-crust);
  font-size: .78rem; color: var(--text-muted);
  margin: 2px 2px 2px 0;
  animation: fadeUp .3s ease both;
}
.file-tag .dot { width: 5px; height: 5px; border-radius: 50%; }
.file-tag.new-file { border-color: rgba(203,166,247,.35); }
.file-tag.new-file .dot { background: var(--accent); }
.file-tag.known-file .dot { background: var(--green); }

/* ════════════════════════════════
   PIPELINE STEPPER
════════════════════════════════ */
.pipeline {
  display: flex; align-items: center;
  margin: 1.5rem 0 1.25rem;
  gap: 0;
}
.pipeline-step {
  display: flex; flex-direction: column; align-items: center;
  flex: 1; position: relative;
}
.pipeline-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 15px;
  left: calc(50% + 16px);
  right: calc(-50% + 16px);
  height: 1px;
  background: var(--bg-surface0);
  z-index: 0;
}
.pipeline-step.done:not(:last-child)::after  { background: var(--green);  }
.pipeline-step.active:not(:last-child)::after { background: var(--bg-surface0); }

.step-node {
  width: 30px; height: 30px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: .72rem; font-weight: 700;
  position: relative; z-index: 1;
  transition: all .3s ease;
  border: 1.5px solid;
}
.pipeline-step.idle   .step-node { background: var(--bg-surface0); border-color: var(--bg-surface0); color: var(--text-dim); }
.pipeline-step.done   .step-node { background: var(--green); border-color: var(--green); color: #1e1e2e; }
.pipeline-step.active .step-node { background: transparent; border-color: var(--accent); color: var(--accent); animation: pulseRing 1.2s ease-in-out infinite; }

.step-label {
  font-size: .68rem; font-weight: 500; letter-spacing: .03em;
  color: var(--text-dim); margin-top: 7px; text-align: center;
  text-transform: uppercase;
}
.pipeline-step.done   .step-label { color: var(--green);  }
.pipeline-step.active .step-label { color: var(--accent); }

/* ════════════════════════════════
   LOADER / SPINNER
════════════════════════════════ */
.loader-card {
  display: flex; align-items: center; gap: 14px;
  padding: 13px 18px;
  background: var(--bg-crust);
  border: 1px solid var(--bg-surface0);
  border-left: 2px solid var(--accent);
  border-radius: 8px;
  margin: .75rem 0;
  animation: fadeUp .35s ease both;
}
.loader-ring {
  width: 20px; height: 20px;
  border: 2px solid var(--bg-surface0);
  border-top-color: var(--accent);
  border-radius: 50%; flex-shrink: 0;
  animation: spin .7s linear infinite;
}
.loader-text { font-size: .875rem; color: var(--text-muted); font-weight: 400; }
.loader-text strong { color: var(--text-main); font-weight: 500; }

/* ════════════════════════════════
   PROGRESS BAR
════════════════════════════════ */
.prog-wrap {
  background: var(--bg-surface0);
  border-radius: 999px; height: 3px;
  overflow: hidden; margin: .25rem 0 .75rem;
}
.prog-fill {
  height: 100%; border-radius: 999px;
  background: linear-gradient(90deg, var(--accent) 0%, var(--blue) 100%);
  background-size: 200% 100%;
  animation: shimmer 2s infinite linear;
  transition: width .45s cubic-bezier(.4,0,.2,1);
}
.prog-label {
  display: flex; justify-content: space-between;
  font-size: .72rem; color: var(--text-dim); margin-bottom: 5px;
}

/* ════════════════════════════════
   SUCCESS / SUMMARY BANNER
════════════════════════════════ */
.summary-banner {
  background: rgba(166,227,161,.06);
  border: 1px solid rgba(166,227,161,.25);
  border-radius: 8px;
  padding: 14px 18px;
  margin-top: .75rem;
  font-size: .875rem;
  color: var(--text-main);
  animation: fadeUp .4s ease both;
}
.summary-banner strong { color: var(--green); }

/* ════════════════════════════════
   OVERVIEW METRICS ROW
════════════════════════════════ */
.metrics-row {
  display: flex; gap: 12px; margin-top: 1.5rem;
}
.metric-tile {
  flex: 1; padding: 16px 20px;
  background: var(--bg-crust);
  border: 1px solid var(--bg-surface0);
  border-radius: 8px;
}
.metric-tile .mt-value {
  font-size: 1.6rem; font-weight: 700;
  color: var(--text-main); letter-spacing: -.03em;
  line-height: 1;
}
.metric-tile .mt-label {
  font-size: .7rem; font-weight: 600; letter-spacing: .08em;
  text-transform: uppercase; color: var(--text-dim); margin-top: 5px;
}

/* ════════════════════════════════
   FILTER ROW
════════════════════════════════ */
.filter-label {
  font-size: .68rem; font-weight: 600;
  letter-spacing: .08em; text-transform: uppercase;
  color: var(--text-dim); margin-bottom: 5px;
}
.count-badge {
  display: inline-block;
  font-size: .75rem; color: var(--text-dim); margin-bottom: .75rem;
}
.count-badge strong { color: var(--accent); }

/* Inputs */
[data-testid="stTextInput"] input {
  background: var(--bg-mantle) !important;
  border: 1px solid var(--bg-surface0) !important;
  border-radius: 7px !important;
  color: var(--text-main) !important;
  font-size: .875rem !important;
  padding: 8px 12px !important;
  transition: border-color .15s ease, box-shadow .15s ease !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(203,166,247,.12) !important;
  outline: none !important;
}
[data-baseweb="select"] > div:first-child {
  background: var(--bg-mantle) !important;
  border: 1px solid var(--bg-surface0) !important;
  border-radius: 7px !important;
  color: var(--text-main) !important;
  font-size: .875rem !important;
  transition: border-color .15s ease !important;
}
[data-baseweb="select"] > div:first-child:hover {
  border-color: var(--accent) !important;
}

/* ════════════════════════════════
   DATAFRAME
════════════════════════════════ */
[data-testid="stDataFrame"] {
  border-radius: 8px !important;
  border: 1px solid var(--bg-surface0) !important;
  overflow: hidden;
}

/* ════════════════════════════════
   RELATIONSHIP CARDS
════════════════════════════════ */
.scroll-box {
  max-height: 520px;
  overflow-y: auto; overflow-x: hidden;
  padding-right: 8px;
  scrollbar-width: thin;
  scrollbar-color: var(--bg-surface0) transparent;
}
.scroll-box::-webkit-scrollbar { width: 5px; }
.scroll-box::-webkit-scrollbar-track { background: transparent; }
.scroll-box::-webkit-scrollbar-thumb { background: var(--bg-surface1); border-radius: 999px; }
.scroll-box::-webkit-scrollbar-thumb:hover { background: var(--accent); }

.rel-card {
  background: var(--bg-crust);
  border: 1px solid var(--bg-surface0);
  border-radius: 8px;
  padding: 18px 20px;
  margin-bottom: 10px;
  border-left: 3px solid;
  animation: slideIn .35s ease both;
  transition: border-color .2s ease, box-shadow .2s ease;
}
.rel-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.3); }
.rel-card.corr  { border-left-color: var(--green);  }
.rel-card.cont  { border-left-color: var(--red);    }
.rel-card.recon { border-left-color: var(--yellow); }

.rel-type-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: .7rem; font-weight: 700; letter-spacing: .06em;
  text-transform: uppercase; padding: 3px 9px;
  border-radius: 4px; margin-bottom: 10px;
}
.corr  .rel-type-badge { background: rgba(166,227,161,.1); color: var(--green);  }
.cont  .rel-type-badge { background: rgba(243,139,168,.1); color: var(--red);    }
.recon .rel-type-badge { background: rgba(249,226,175,.1); color: var(--yellow); }

.rel-explanation {
  font-size: .875rem; color: var(--text-muted);
  line-height: 1.65; margin-bottom: 14px;
}
.fact-pair { display: flex; gap: 10px; flex-wrap: wrap; }
.fact-card {
  flex: 1; min-width: 200px;
  background: var(--bg-base);
  border: 1px solid var(--bg-surface0);
  border-radius: 6px; padding: 12px 14px;
}
.fact-card .fc-source {
  font-size: .68rem; font-weight: 600; letter-spacing: .06em;
  text-transform: uppercase; color: var(--accent); margin-bottom: 7px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.fact-card .fc-metric {
  font-size: .875rem; font-weight: 600; color: var(--text-main);
  margin-bottom: 2px;
}
.fact-card .fc-value  { font-size: .875rem; color: var(--text-muted); }
.fact-card .fc-ctx    { font-size: .75rem; color: var(--text-dim); margin: 4px 0; }
.fact-card .fc-quote  {
  font-size: .72rem; color: var(--text-dim);
  border-left: 2px solid var(--bg-surface0);
  padding-left: 8px; margin-top: 8px; line-height: 1.55;
  font-style: italic;
}

/* ════════════════════════════════
   SUMMARY STAT ROW (Reasoning)
════════════════════════════════ */
.rel-summary-row {
  display: flex; gap: 10px; margin-bottom: 1.25rem;
}
.rel-stat {
  flex: 1; padding: 12px 16px;
  background: var(--bg-crust);
  border: 1px solid var(--bg-surface0);
  border-radius: 7px;
  text-align: left;
}
.rel-stat .rs-value {
  font-size: 1.5rem; font-weight: 700;
  letter-spacing: -.03em; line-height: 1;
}
.rel-stat .rs-label {
  font-size: .68rem; font-weight: 600; letter-spacing: .07em;
  text-transform: uppercase; color: var(--text-dim); margin-top: 4px;
}
.rs-corr  .rs-value { color: var(--green);  }
.rs-cont  .rs-value { color: var(--red);    }
.rs-recon .rs-value { color: var(--yellow); }

/* ════════════════════════════════
   EMPTY STATE
════════════════════════════════ */
.empty-state {
  text-align: center; padding: 56px 24px;
  animation: fadeUp .5s ease both;
}
.empty-icon {
  width: 44px; height: 44px; margin: 0 auto 14px;
  opacity: .25;
}
.empty-state h3 {
  font-size: 1rem; font-weight: 600;
  color: var(--text-muted); margin-bottom: 6px;
}
.empty-state p {
  font-size: .85rem; color: var(--text-dim);
  max-width: 340px; margin: 0 auto; line-height: 1.6;
}

/* ════════════════════════════════
   BUTTONS
════════════════════════════════ */
.stButton button {
  border-radius: 7px !important;
  font-weight: 500 !important;
  font-size: .875rem !important;
  letter-spacing: .01em !important;
  transition: all .2s ease !important;
}
.stButton button[kind="primary"] {
  background: var(--accent) !important;
  border: none !important;
  color: #1e1e2e !important;
  padding: 9px 22px !important;
}
.stButton button[kind="primary"]:hover {
  background: var(--accent-dark) !important;
  box-shadow: 0 4px 14px rgba(203,166,247,.35) !important;
  transform: translateY(-1px) !important;
}
.stButton button[kind="secondary"] {
  background: var(--bg-crust) !important;
  border: 1px solid var(--bg-surface0) !important;
  color: var(--text-muted) !important;
}
.stButton button[kind="secondary"]:hover {
  border-color: var(--red) !important;
  color: var(--red) !important;
  transform: translateY(-1px) !important;
}

/* ════════════════════════════════
   ALERTS
════════════════════════════════ */
[data-testid="stAlert"] { border-radius: 7px !important; border: none !important; }

/* ════════════════════════════════
   FOOTER
════════════════════════════════ */
.app-footer {
  margin-top: 3rem; padding-top: 1.25rem;
  border-top: 1px solid var(--bg-surface0);
  text-align: center;
  font-size: .75rem; color: var(--text-dim);
  letter-spacing: .02em;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

from extractor import extract_text_from_pdf, extract_facts
from analyzer import analyze_facts

# ─────────────────────────────────────────────────────────────
# API KEY
# ─────────────────────────────────────────────────────────────
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("API key missing. Set GEMINI_API_KEY in your .env file.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
_defaults = {
    "facts": [],
    "processed_files": set(),
    "relationships": [],
    "processing": False,
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Financial":     "#cba6f7",
    "Operational":   "#89b4fa",
    "Macroeconomic": "#94e2d5",
    "Leadership":    "#f9e2af",
    "Legal":         "#fab387",
    "Technology":    "#a6e3a1",
}
def cat_color(cat: str) -> str:
    return CAT_COLORS.get(cat, "#a6adc8")

def sidebar_cat_bars(df: pd.DataFrame) -> str:
    if "category" not in df.columns or df.empty:
        return ""
    counts = df["category"].value_counts()
    total  = max(len(df), 1)
    out = ""
    for cat, cnt in counts.items():
        pct = cnt / total * 100
        col = cat_color(cat)
        out += f"""
        <div class="stat-bar-wrap">
          <div class="stat-bar-label">
            <strong style="color:{col};">{cat}</strong>
            <span>{cnt}</span>
          </div>
          <div class="stat-bar">
            <div class="stat-bar-fill" style="width:{pct}%;background:{col};"></div>
          </div>
        </div>"""
    return out

# SVG icons (inline, no emoji)
ICON_DB = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v4c0 1.657 4.03 3 9 3s9-1.343 9-3V5"/><path d="M3 9v4c0 1.657 4.03 3 9 3s9-1.343 9-3V9"/><path d="M3 13v4c0 1.657 4.03 3 9 3s9-1.343 9-3v-4"/></svg>'
ICON_LOCK = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>'
ICON_SEARCH = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>'
ICON_CHECK = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
      <div class="sidebar-wordmark">Fact <span>Knowledge Layer</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Knowledge Base</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Documents",    len(st.session_state.processed_files))
    c2.metric("Facts",        len(st.session_state.facts))
    st.metric("Relationships", len(st.session_state.relationships))

    if st.session_state.facts:
        df_all = pd.DataFrame(st.session_state.facts)
        st.markdown('<div class="sidebar-section-label">By Category</div>', unsafe_allow_html=True)
        st.markdown(sidebar_cat_bars(df_all), unsafe_allow_html=True)

    if st.session_state.processed_files:
        st.markdown('<div class="sidebar-section-label">Indexed Documents</div>', unsafe_allow_html=True)
        for fname in sorted(st.session_state.processed_files):
            short = fname if len(fname) <= 26 else fname[:23] + "…"
            st.markdown(
                f"<div class='doc-entry'>"
                f"<div class='status-dot' style='background:var(--green);'></div>"
                f"<div class='doc-name'>{short}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Reset Knowledge Base", use_container_width=True, type="secondary"):
        for k in ["facts", "relationships"]:
            st.session_state[k] = []
        st.session_state.processed_files = set()
        st.session_state.processing = False
        st.rerun()

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div class="page-title">Superjoin <em>Fact Layer</em></div>
  <div class="page-subtitle">
    Incremental document ingestion with AI-powered cross-document fact extraction,
    corroboration detection, and contradiction resolution.
  </div>
</div>
""", unsafe_allow_html=True)

tab_ingest, tab_explore, tab_reasoning = st.tabs(["Ingest", "Explorer", "Reasoning"])


# ══════════════════════════════════════════════════════════════
# TAB 1  —  INGEST
# ══════════════════════════════════════════════════════════════
with tab_ingest:
    st.markdown('<div class="section-title">Upload Documents</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Select one or more PDF files to add to the knowledge base",
        type="pdf",
        accept_multiple_files=True,
    )

    if uploaded_files:
        new_files   = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
        known_files = [f for f in uploaded_files if f.name in st.session_state.processed_files]

        parts = []
        if new_files:
            tags = "".join(
                f"<span class='file-tag new-file'>"
                f"<span class='dot'></span>{f.name}</span>"
                for f in new_files
            )
            parts.append(
                f"<div class='file-status-block'>"
                f"<div class='file-status-label'>Queued for processing</div>{tags}</div>"
            )
        if known_files:
            tags = "".join(
                f"<span class='file-tag known-file'>"
                f"<span class='dot'></span>{f.name}</span>"
                for f in known_files
            )
            parts.append(
                f"<div class='file-status-block'>"
                f"<div class='file-status-label'>Already indexed</div>{tags}</div>"
            )
        if parts:
            st.markdown(
                f"<div class='file-status-grid'>{''.join(parts)}</div>",
                unsafe_allow_html=True,
            )

    col_btn, col_hint = st.columns([1, 4])
    with col_btn:
        run_btn = st.button("Process Documents", type="primary", use_container_width=True)
    with col_hint:
        st.markdown(
            "<div style='padding-top:9px;font-size:.8rem;color:var(--text-dim);'>"
            "Requires at least 2 documents to enable cross-document reasoning."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Processing pipeline ──────────────────────────────────
    if run_btn:
        if not uploaded_files:
            st.warning("No files selected. Please upload at least one PDF.")
        else:
            new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
            if not new_files:
                st.info("All selected documents are already indexed in the knowledge base.")
            else:
                st.session_state.processing = True
                n = len(new_files)

                STEPS = ["Parse", "Extract", "Graph", "Complete"]

                pipeline_ph = st.empty()
                loader_ph   = st.empty()
                progress_ph = st.empty()

                def render_pipeline(active: int):
                    html = ""
                    for i, label in enumerate(STEPS):
                        if i < active:
                            css, node = "done",   ICON_CHECK
                        elif i == active:
                            css, node = "active", str(i + 1)
                        else:
                            css, node = "idle",   str(i + 1)
                        html += (
                            f"<div class='pipeline-step {css}'>"
                            f"<div class='step-node'>{node}</div>"
                            f"<div class='step-label'>{label}</div>"
                            f"</div>"
                        )
                    pipeline_ph.markdown(
                        f"<div class='pipeline'>{html}</div>",
                        unsafe_allow_html=True,
                    )

                def show_loader(msg: str):
                    loader_ph.markdown(
                        f"<div class='loader-card'>"
                        f"<div class='loader-ring'></div>"
                        f"<div class='loader-text'>{msg}</div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                def show_progress(current: int, total: int):
                    pct = int(current / max(total, 1) * 100)
                    progress_ph.markdown(
                        f"<div class='prog-label'>"
                        f"<span>Documents processed</span><span>{current} / {total}</span>"
                        f"</div>"
                        f"<div class='prog-wrap'>"
                        f"<div class='prog-fill' style='width:{pct}%;'></div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                render_pipeline(0)

                import concurrent.futures
                def process_file(file_obj):
                    text = extract_text_from_pdf(file_obj.read())
                    extracted = extract_facts(text, file_obj.name, api_key)
                    return file_obj.name, extracted

                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = {executor.submit(process_file, f): f for f in new_files}
                    
                    for i, future in enumerate(concurrent.futures.as_completed(futures)):
                        render_pipeline(1)
                        file_name, new_facts = future.result()
                        show_loader(
                            f"Extracting facts from <strong>{file_name}</strong> "
                            f"<span style='color:var(--text-dim);font-size:.8rem;'>"
                            f"via Gemini 2.5 Flash</span>"
                        )
                        st.session_state.facts.extend(new_facts)
                        st.session_state.processed_files.add(file_name)
                        show_progress(i + 1, n)

                if len(st.session_state.processed_files) >= 2:
                    render_pipeline(2)
                    show_loader(
                        "Building cross-document knowledge graph "
                        "<span style='color:var(--text-dim);font-size:.8rem;'>"
                        "via Gemini 2.5 Pro</span>"
                    )
                    st.session_state.relationships = analyze_facts(st.session_state.facts, api_key)

                render_pipeline(3)
                loader_ph.empty()
                progress_ph.empty()
                st.session_state.processing = False

                total_facts = len(st.session_state.facts)
                total_docs  = len(st.session_state.processed_files)
                total_rels  = len(st.session_state.relationships)
                st.markdown(
                    f"<div class='summary-banner'>"
                    f"Ingested <strong>{n} document{'s' if n > 1 else ''}</strong>. "
                    f"Knowledge base now contains "
                    f"<strong>{total_facts} facts</strong> across "
                    f"<strong>{total_docs} documents</strong>"
                    f"{f' with <strong>{total_rels} cross-document relationships</strong>' if total_rels else ''}."
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # ── KB overview ──────────────────────────────────────────
    if st.session_state.processed_files:
        docs  = len(st.session_state.processed_files)
        facts = len(st.session_state.facts)
        rels  = len(st.session_state.relationships)
        st.markdown(
            f"<div class='metrics-row'>"
            f"<div class='metric-tile'><div class='mt-value'>{docs}</div><div class='mt-label'>Documents</div></div>"
            f"<div class='metric-tile'><div class='mt-value'>{facts}</div><div class='mt-label'>Facts Extracted</div></div>"
            f"<div class='metric-tile'><div class='mt-value'>{rels}</div><div class='mt-label'>Relationships</div></div>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════
# TAB 2  —  EXPLORER
# ══════════════════════════════════════════════════════════════
with tab_explore:
    st.markdown('<div class="section-title">Fact Database</div>', unsafe_allow_html=True)

    if not st.session_state.facts:
        st.markdown(
            f"<div class='empty-state'>"
            f"<div class='empty-icon' style='color:var(--text-dim);'>{ICON_DB}</div>"
            f"<h3>No facts extracted yet</h3>"
            f"<p>Switch to the Ingest tab and process at least one document to populate the knowledge base.</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        df = pd.DataFrame(st.session_state.facts)

        col_s, col_d, col_c = st.columns([2, 2, 2])
        with col_s:
            st.markdown('<div class="filter-label">Search</div>', unsafe_allow_html=True)
            search_q = st.text_input("s", placeholder="Filter by entity, value, metric…",
                                     label_visibility="collapsed")
        with col_d:
            st.markdown('<div class="filter-label">Source Document</div>', unsafe_allow_html=True)
            doc_filter = st.multiselect("d", options=sorted(df["document"].unique()),
                                        label_visibility="collapsed")
        with col_c:
            st.markdown('<div class="filter-label">Category</div>', unsafe_allow_html=True)
            if "category" in df.columns:
                cat_filter = st.multiselect("c", options=sorted(df["category"].unique()),
                                             label_visibility="collapsed")
            else:
                cat_filter = []

        # Apply filters
        fdf = df.copy()
        if search_q:
            mask = fdf.apply(
                lambda row: row.astype(str).str.contains(search_q, case=False, na=False).any(),
                axis=1,
            )
            fdf = fdf[mask]
        if doc_filter:
            fdf = fdf[fdf["document"].isin(doc_filter)]
        if cat_filter and "category" in fdf.columns:
            fdf = fdf[fdf["category"].isin(cat_filter)]

        st.markdown(
            f"<div class='count-badge'>Showing <strong>{len(fdf)}</strong> of {len(df)} facts</div>",
            unsafe_allow_html=True,
        )

        col_cfg = {
            "id":           st.column_config.TextColumn("ID",           width="small"),
            "document":     st.column_config.TextColumn("Source",       width="medium"),
            "category":     st.column_config.TextColumn("Category",     width="small"),
            "entity":       st.column_config.TextColumn("Entity",       width="medium"),
            "metric":       st.column_config.TextColumn("Metric",       width="medium"),
            "value":        st.column_config.TextColumn("Value",        width="small"),
            "context":      st.column_config.TextColumn("Context",      width="medium"),
            "source_quote": st.column_config.TextColumn("Source Quote", width="large"),
        }
        st.dataframe(
            fdf, use_container_width=True, hide_index=True,
            height=min(max(240, len(fdf) * 38 + 58), 500),
            column_config=col_cfg,
        )

        if "category" in fdf.columns and not fdf.empty:
            st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="filter-label">Category Distribution</div>', unsafe_allow_html=True)
            st.markdown(sidebar_cat_bars(fdf), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3  —  REASONING
# ══════════════════════════════════════════════════════════════
with tab_reasoning:
    st.markdown('<div class="section-title">Cross-Document Reasoning</div>', unsafe_allow_html=True)

    if len(st.session_state.processed_files) < 2:
        st.markdown(
            f"<div class='empty-state'>"
            f"<div class='empty-icon' style='color:var(--text-dim);'>{ICON_LOCK}</div>"
            f"<h3>Requires multiple documents</h3>"
            f"<p>Process at least two documents in the Ingest tab to enable AI-powered "
            f"cross-document contradiction and corroboration analysis.</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    elif not st.session_state.relationships:
        st.markdown(
            f"<div class='empty-state'>"
            f"<div class='empty-icon' style='color:var(--text-dim);'>{ICON_SEARCH}</div>"
            f"<h3>No relationships detected</h3>"
            f"<p>The reasoning engine found no cross-document relationships. "
            f"Try uploading documents that cover overlapping topics.</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        rels = st.session_state.relationships

        corr_n  = sum(1 for r in rels if r["relationship_type"] == "Corroboration")
        cont_n  = sum(1 for r in rels if r["relationship_type"] == "Contradiction")
        recon_n = sum(1 for r in rels if r["relationship_type"] == "Reconciled Contradiction")

        st.markdown(
            f"<div class='rel-summary-row'>"
            f"<div class='rel-stat rs-corr'><div class='rs-value'>{corr_n}</div><div class='rs-label'>Corroborations</div></div>"
            f"<div class='rel-stat rs-cont'><div class='rs-value'>{cont_n}</div><div class='rs-label'>Contradictions</div></div>"
            f"<div class='rel-stat rs-recon'><div class='rs-value'>{recon_n}</div><div class='rs-label'>Reconciled</div></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        col_tf, _ = st.columns([2, 4])
        with col_tf:
            type_filter = st.multiselect(
                "Filter by type",
                options=["Corroboration", "Contradiction", "Reconciled Contradiction"],
                default=[],
                placeholder="All relationship types",
            )

        filtered_rels = rels if not type_filter else [
            r for r in rels if r["relationship_type"] in type_filter
        ]

        st.markdown(
            f"<div class='count-badge'>Showing <strong>{len(filtered_rels)}</strong> of {len(rels)} relationships</div>",
            unsafe_allow_html=True,
        )

        def _fact_card(f) -> str:
            if not f:
                return "<div class='fact-card'><span style='color:var(--text-dim);font-size:.8rem;'>Fact unavailable</span></div>"
            return (
                f"<div class='fact-card'>"
                f"<div class='fc-source'>{f['document']}</div>"
                f"<div class='fc-metric'>{f['metric']}</div>"
                f"<div class='fc-value'>{f['value']}</div>"
                f"<div class='fc-ctx'>{f['context']}</div>"
                f"<div class='fc-quote'>{f['source_quote']}</div>"
                f"</div>"
            )

        TYPE_CSS   = {"Corroboration": "corr", "Contradiction": "cont", "Reconciled Contradiction": "recon"}
        TYPE_LABEL = {"Corroboration": "Corroboration", "Contradiction": "Contradiction", "Reconciled Contradiction": "Reconciled Contradiction"}

        cards_html = ""
        for rel in filtered_rels:
            rt   = rel["relationship_type"]
            css  = TYPE_CSS.get(rt, "corr")
            label = TYPE_LABEL.get(rt, rt)

            f1 = next((f for f in st.session_state.facts if f["id"] == rel["fact_1_id"]), None)
            f2 = next((f for f in st.session_state.facts if f["id"] == rel["fact_2_id"]), None)

            cards_html += (
                f"<div class='rel-card {css}'>"
                f"<span class='rel-type-badge'>{label}</span>"
                f"<div class='rel-explanation'>{rel['explanation']}</div>"
                f"<div class='fact-pair'>{_fact_card(f1)}{_fact_card(f2)}</div>"
                f"</div>"
            )

        st.markdown(f"<div class='scroll-box'>{cards_html}</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown(
    "<div class='app-footer'>Superjoin Engineering Assignment &nbsp;&middot;&nbsp; Gemini 2.5</div>",
    unsafe_allow_html=True,
)
