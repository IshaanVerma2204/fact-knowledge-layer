import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import time

load_dotenv()

st.set_page_config(page_title="Fact Knowledge Layer", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (ANIMATIONS & STYLING) ---
st.markdown("""
<style>
/* Global Fade In Animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Apply animation to tabs and main content */
.stTabs [data-baseweb="tab-panel"], .main .block-container {
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Metric Cards Hover Effect */
div[data-testid="stMetric"] {
    background-color: #1e1e2e;
    border: 1px solid #313244;
    padding: 15px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.3);
    border-color: #cba6f7;
}

/* Custom Reasoning Cards */
.reasoning-card {
    background: linear-gradient(145deg, #1e1e2e, #181825);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    border-left: 6px solid;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeIn 0.5s ease-out;
}
.reasoning-card:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.rc-corr { border-left-color: #a6e3a1; }
.rc-corr h4 { color: #a6e3a1; margin-top: 0; font-weight: 600; }

.rc-cont { border-left-color: #f38ba8; }
.rc-cont h4 { color: #f38ba8; margin-top: 0; font-weight: 600; }

.rc-recon { border-left-color: #f9e2af; }
.rc-recon h4 { color: #f9e2af; margin-top: 0; font-weight: 600; }

.explanation-text {
    font-size: 1.1em;
    color: #cdd6f4;
    line-height: 1.5;
}

.fact-box {
    background-color: #11111b;
    padding: 15px;
    border-radius: 8px;
    margin-top: 15px;
    border: 1px solid #313244;
    color: #a6adc8;
}

/* Button Pulse Animation */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}
.stButton button[kind="primary"] {
    transition: all 0.3s ease;
    width: 100%;
}
.stButton button[kind="primary"]:hover {
    animation: pulse 1s infinite;
    box-shadow: 0 0 15px rgba(203, 166, 247, 0.4);
}
</style>
""", unsafe_allow_html=True)

from extractor import extract_text_from_pdf, extract_facts
from analyzer import analyze_facts

# --- LOAD API KEY ---
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    st.error("🚨 API Key missing! Please ensure GEMINI_API_KEY is set in your .env file.")
    st.stop()

# --- STATE MANAGEMENT ---
if "facts" not in st.session_state: st.session_state.facts = []
if "processed_files" not in st.session_state: st.session_state.processed_files = set()
if "relationships" not in st.session_state: st.session_state.relationships = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #cba6f7;'>⚡ Fact Engine</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📊 Knowledge Stats")
    col1, col2 = st.columns(2)
    col1.metric("📚 Documents", len(st.session_state.processed_files))
    col2.metric("🧠 Facts", len(st.session_state.facts))
    
    st.markdown("---")
    if st.button("🗑️ Reset Engine", use_container_width=True):
        st.session_state.facts = []
        st.session_state.processed_files = set()
        st.session_state.relationships = []
        st.rerun()

# --- MAIN APP ---
st.markdown("<h1 style='text-align: center;'>Superjoin Fact Layer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a6adc8; font-size: 1.2em;'>An intelligent reasoning engine that incrementally ingests documents and dynamically resolves conflicts.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

tab_ingest, tab_explore, tab_reasoning = st.tabs([
    "📥 Ingest", 
    "🔍 Explorer", 
    "🤝 Reasoning"
])

# --- TAB 1: INGESTION ---
with tab_ingest:
    st.markdown("### 📤 Upload to Knowledge Base")
    
    uploaded_files = st.file_uploader("Drag and drop your PDFs here", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
    
    if st.button("🚀 Process Documents", type="primary"):
        if not uploaded_files:
            st.warning("Please upload at least one PDF.")
        else:
            new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_files]
            
            if not new_files:
                st.info("✨ All uploaded documents are already in the Knowledge Base!")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, file in enumerate(new_files):
                    status_text.text(f"Extracting & Categorizing: {file.name}...")
                    
                    # Small animation delay for smooth UI feedback
                    time.sleep(0.5) 
                    
                    text = extract_text_from_pdf(file.read())
                    new_facts = extract_facts(text, file.name, api_key)
                    st.session_state.facts.extend(new_facts)
                    st.session_state.processed_files.add(file.name)
                    
                    progress_bar.progress((i + 1) / len(new_files))
                
                status_text.text("Building Cross-Document Graph...")
                
                if len(st.session_state.processed_files) >= 2:
                    st.session_state.relationships = analyze_facts(st.session_state.facts, api_key)
                
                progress_bar.empty()
                status_text.empty()
                
                st.success(f"🎉 Successfully ingested {len(new_files)} document(s)!")
                st.balloons()
                time.sleep(1.5)
                st.rerun()

# --- TAB 2: FACT EXPLORER ---
with tab_explore:
    st.markdown("### 🗃️ Fact Database")
    
    if not st.session_state.facts:
        st.info("No facts extracted yet. Head over to the Ingest tab.")
    else:
        df = pd.DataFrame(st.session_state.facts)
        
        col1, col2 = st.columns(2)
        with col1:
            doc_filter = st.multiselect("Filter by Source Document", options=df['document'].unique())
        with col2:
            if 'category' in df.columns:
                cat_filter = st.multiselect("Filter by AI Category", options=df['category'].unique())
            else:
                cat_filter = []
                
        filtered_df = df
        if doc_filter:
            filtered_df = filtered_df[filtered_df['document'].isin(doc_filter)]
        if cat_filter and 'category' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['category'].isin(cat_filter)]
            
        st.dataframe(
            filtered_df, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "id": st.column_config.TextColumn("Fact ID", width="small"),
                "document": st.column_config.TextColumn("Source Doc", width="medium"),
                "category": st.column_config.TextColumn("Category", width="small"),
                "source_quote": st.column_config.TextColumn("Original Quote", width="large")
            }
        )

# --- TAB 3: REASONING ---
with tab_reasoning:
    st.markdown("### 🧠 AI Fact Reconciliation")
    
    if len(st.session_state.processed_files) < 2:
        st.info("Upload at least 2 documents to unlock cross-document reasoning.")
    elif not st.session_state.relationships:
        st.warning("No cross-document relationships found yet. Try uploading more diverse documents.")
    else:
        for rel in st.session_state.relationships:
            rel_type = rel['relationship_type']
            
            if rel_type == 'Corroboration':
                css_class = "rc-corr"
                icon = "✅"
            elif rel_type == 'Contradiction':
                css_class = "rc-cont"
                icon = "❌"
            else:
                css_class = "rc-recon"
                icon = "⚠️"
                
            f1 = next((f for f in st.session_state.facts if f['id'] == rel['fact_1_id']), None)
            f2 = next((f for f in st.session_state.facts if f['id'] == rel['fact_2_id']), None)
            
            f1_html = ""
            if f1:
                f1_html = f"""
                <div class="fact-box">
                    <span style="color: #cba6f7; font-size: 0.9em;">📄 {f1['document']}</span><br>
                    <strong>{f1['metric']}</strong>: {f1['value']}<br>
                    <em>Context: {f1['context']}</em><br><br>
                    <span style="font-size: 0.85em; color: #6c7086;">"{f1['source_quote']}"</span>
                </div>
                """
                
            f2_html = ""
            if f2:
                f2_html = f"""
                <div class="fact-box">
                    <span style="color: #cba6f7; font-size: 0.9em;">📄 {f2['document']}</span><br>
                    <strong>{f2['metric']}</strong>: {f2['value']}<br>
                    <em>Context: {f2['context']}</em><br><br>
                    <span style="font-size: 0.85em; color: #6c7086;">"{f2['source_quote']}"</span>
                </div>
                """

            html_card = f"""
            <div class="reasoning-card {css_class}">
                <h4>{icon} {rel_type}</h4>
                <div class="explanation-text">{rel['explanation']}</div>
                <div style="display: flex; gap: 20px; margin-top: 15px;">
                    <div style="flex: 1;">{f1_html}</div>
                    <div style="flex: 1;">{f2_html}</div>
                </div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #6c7086; font-size: 0.9em;'>Built for Superjoin Assignment</p>", unsafe_allow_html=True)
