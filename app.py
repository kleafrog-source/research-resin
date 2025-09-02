"""
Resin Simulation App - Main Entry Point

This is the main application file that brings together all the modular components.
"""
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import io
import base64
from pathlib import Path

# Import from our modules
from src.models import ComputationalState, IonFirmware
from src.core.simulation import (
    BASE_RESIN_PROPS, 
    apply_firmware, 
    generate_single_ion_states,
    run_program, 
    simulate_osmotic_degradation, 
    mixed_ion_state
)
from src.core.prediction import PropertyPredictor

# Import page modules
from src.ui.pages.data_view import show_data_view
from src.ui.pages.simulation import show_simulation_page
from src.ui.pages.analysis import show_analysis_page
from src.ui.pages.import_export import show_import_export_page
from src.ui.pages.prediction import show_prediction_interface
from src.ui.pages.advanced_analysis import show_advanced_analysis
from src.ui.pages.glossary_page import show_glossary_page
from src.ui.pages.toc_removal_page import show_toc_removal_page

# Set page config
st.set_page_config(
    page_title="Ion Exchange Research",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set page title and description
st.title("🧪 Ion Exchange in Polymer Resins Research")
st.markdown("""
    ### Simulation and Analysis of Ion Exchange in Ion-Exchange Resins
    
    This application simulates the behavior of ion-exchange resins when interacting with various ions.
    You can analyze the state of the resin, run simulations, and visualize the results.
""")

# Initialize session state
if 'resin_props' not in st.session_state:
    st.session_state.resin_props = BASE_RESIN_PROPS.copy()

# Generate ion states once and store in session state
if 'ion_states' not in st.session_state:
    st.session_state.ion_states = generate_single_ion_states(st.session_state.resin_props)

# Initialize predictor if not exists
if 'predictor' not in st.session_state:
    st.session_state.predictor = PropertyPredictor()
    # Train models with initial ion states
    st.session_state.predictor.train_models(st.session_state.ion_states)

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a section:",
    ["Resin Data", "Simulation", "TOC Removal", "Analysis", "Prediction", "Advanced Analysis", "Glossary", "Import/Export"],
    index=0
)

# Load the appropriate page based on selection
if page == "Resin Data":
    show_data_view(st.session_state.resin_props, st.session_state.ion_states)
    
elif page == "Simulation":
    show_simulation_page(st.session_state.resin_props)

elif page == "TOC Removal":
    show_toc_removal_page()
    
elif page == "Analysis":
    show_analysis_page(st.session_state.resin_props)
    
elif page == "Prediction":
    show_prediction_interface(st.session_state.predictor)
    
elif page == "Advanced Analysis":
    show_advanced_analysis(st.session_state.ion_states)

elif page == "Glossary":
    show_glossary_page()
    
elif page == "Import/Export":
    show_import_export_page(st.session_state.resin_props, st.session_state.ion_states)

# Add footer
st.sidebar.markdown("---")
st.sidebar.info(
    """
    ### About the App
    Version 1.0.0
    Developed for ion exchange research
    2023
    """
)

# Add some custom CSS
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)