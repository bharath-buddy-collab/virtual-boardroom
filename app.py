import streamlit as st
import pandas as pd
import os
import vertexai
from dotenv import load_dotenv
import logging
import shutil

# --- IMPORT ARCHITECTURE ---
from manager_agent import BoardroomManager
from memory_engine import MemoryService
from observability import setup_observability

# --- 1. CONFIGURATION & INIT ---
load_dotenv()
setup_observability() 

st.set_page_config(
    page_title="Virtual Boardroom",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Vertex AI
project_id = os.getenv("GCP_PROJECT_ID")
if project_id:
    try:
        vertexai.init(project=project_id, location="us-central1")
    except Exception as e:
        st.error(f"Vertex AI Init Error: {e}")

# --- 2. STATE MANAGEMENT ---
memory = MemoryService()
if "state" not in st.session_state:
    st.session_state.state = memory.load_state()
    if st.session_state.state.ceo_data:
        st.toast("🧠 Strategy restored from corporate memory.", icon="💾")

state = st.session_state.state

# --- 3. SIDEBAR (INPUTS) ---
with st.sidebar:
    st.header("🏢 Business Context")
    st.caption("Define the business parameters.")
    
    # Context Inputs
    niche_input = st.text_input("Niche", value=state.niche, placeholder="e.g. Fintech Startup")
    goal_input = st.text_input("Goal", value=state.goal, placeholder="e.g. Reduce server costs")
    location_input = st.text_input("📍 Location", value="London, UK")
    
    # Currency Selection
    currency_input = st.selectbox("💱 Currency", ["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)"])
    
    st.divider()
    uploaded_file = st.file_uploader("Financials (CSV)", type=["csv"])
    
    st.markdown("---")
    if st.button("🧹 Reset System", use_container_width=True):
        memory.clear_memory()
        st.session_state.clear()
        st.rerun()

# --- 4. MAIN DASHBOARD ---
st.title("👔 The Virtual Boardroom")
st.caption("Level 3 Multi-Agent System (Manager-Worker Architecture)")

# --- DATA HANDLING (CLOUD FIX) ---
# Determine the writable path based on environment
CSV_PATH = "/tmp/financials.csv" if os.path.exists("/tmp") else "financials.csv"

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        # Save to writable location (Cloud Fix)
        df.to_csv(CSV_PATH, index=False)
        
        with st.expander("📊 Data Preview", expanded=False):
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()
else:
    # If no upload, check if a sample exists in the read-only app folder
    # and copy it to tmp for the agents to use
    if os.path.exists("financials.csv") and not os.path.exists(CSV_PATH):
        shutil.copy("financials.csv", CSV_PATH)
        
    st.info("👋 Welcome! Please upload your financial data to begin.")
    # Stop execution until data is present
    st.stop()

# --- 5. EXECUTION ENGINE (The Manager) ---
if st.button("🚀 Execute Strategy", type="primary", use_container_width=True):
    # Update State with latest inputs
    state.niche = niche_input
    state.goal = goal_input
    
    try:
        # A. CONTEXT ENGINEERING: COMPACTION
        # Before running new logic, we compact the OLD strategy into history.
        if state.ceo_data:
            with st.spinner("🧹 Compacting previous context..."):
                memory.compact_context(state)
        
        # B. INSTANTIATE MANAGER
        manager = BoardroomManager()
        
        # C. PHASE 1: ROUTING
        with st.status("🚦 Manager is analyzing request...", expanded=True) as s:
            user_request = f"Goal: {state.goal}. Niche: {state.niche}"
            intent = manager.route_request(user_request)
            s.update(label=f"✅ Intent Classified: {intent}", state="complete")
        
        # D. PHASE 2: EXECUTION
        if intent == "CHAT":
             st.info("👋 Hello! Please upload data or ask for a specific strategy.")
             
        elif intent in ["FINANCE", "MARKETING", "STRATEGY"]:
            
            with st.status("⚙️ Orchestrating Agents...", expanded=True) as s:
                st.write("👨‍💼 CFO is performing Python analysis...")
                st.write("👩‍🎨 CMO is researching local trends...")
                st.write("👑 CEO is synthesizing the directive...")
                
                # Note: csv_context points to the filename; workers will auto-detect /tmp
                results = manager.execute_workflow(
                    niche=state.niche,
                    goal=state.goal,
                    location=location_input,
                    currency=currency_input, 
                    csv_context="financials.csv" 
                )
                
                # Update Active State
                state.cfo_data = results["cfo"]
                state.cmo_data = results["cmo"]
                state.ceo_data = results["ceo"]
                
                s.update(label="✅ Strategy Developed", state="complete")

            # Save to Memory (New state + Compacted history)
            memory.save_state(state)
            st.rerun()

    except Exception as e:
        st.error(f"❌ System Error: {e}")

# --- 6. RESULTS DISPLAY ---
if state.ceo_data:
    st.divider()
    
    # 2-Column Layout for Workers
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**💰 CFO Findings**\n\n{state.cfo_data}")
    with c2:
        st.success(f"**🎨 CMO Strategy**\n\n{state.cmo_data}")
    
    # Full Width for CEO
    st.warning(f"**👑 CEO Directive**\n\n{state.ceo_data}")
    
    # Show History (Proof of Compaction)
    if state.history:
        with st.expander("📜 Historical Context (Compacted Memory)"):
            for item in state.history:
                st.text(item)