import streamlit as st
import state
import ui

# --- 1. SET UP PAGE ---
st.set_page_config(layout="wide")
st.title("🏗️ Technical Construction Suitability Advisor")

# --- 2. INITIALIZE STATE ---
# This is the most important step. It runs once and sets up 
# st.session_state, which prevents the form from resetting.
state.initialize_state()

# --- 3. CREATE TABS ---
tab1, tab2, tab3 = st.tabs([
    "Enter Site Details (Measure)", 
    "View Analysis Report", 
    "Check Project Requirements"
])

# --- 4. RENDER TABS ---
with tab1:
    ui.render_input_tab()

with tab2:
    ui.render_report_tab()
    
with tab3:
    ui.render_requirements_tab()