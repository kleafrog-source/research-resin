"""
This module defines the TOC Removal Simulation page.
"""
import streamlit as st
from ...models.state import Resin
from ...core.simulation import simulate_toc_removal

def show_toc_removal_page():
    """
    Displays the TOC Removal Simulation interface.
    """
    st.header("🌊 TOC Removal Simulation")
    st.markdown("""
    Simulate the removal of Total Organic Carbon (TOC) from water using different ion-exchange resins.
    This feature helps in selecting the appropriate resin for treating water contaminated with organic molecules.
    """)

    # --- INPUTS ---
    st.subheader("Simulation Parameters")
    col1, col2 = st.columns(2)

    with col1:
        # Load resins and filter for those suitable for TOC removal (e.g., macroporous)
        try:
            # Corrected path assuming the pages are in a subdirectory
            resins = Resin.load_from_json('src/core/resin_datasets.json')
            toc_resins = [r for r in resins if r.structure == "Macroporous"]
            if not toc_resins:
                toc_resins = resins # Fallback to all resins if no macroporous are found
            resin_names = [r.name for r in toc_resins]
            selected_resin_name = st.selectbox("Select Resin", resin_names)
        except Exception as e:
            st.error(f"Could not load resins: {e}")
            return

        contaminant = st.selectbox("Select Organic Contaminant", ["Tannic Acid", "Humic Acid", "Fulvic Acid"])

    with col2:
        initial_toc = st.number_input("Initial TOC (mg/L)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        ph = st.slider("Water pH", min_value=2.0, max_value=10.0, value=7.0, step=0.1)

    # --- SIMULATION ---
    if st.button("Run TOC Removal Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            selected_resin = next((r for r in resins if r.name == selected_resin_name), None)
            if selected_resin:
                results = simulate_toc_removal(
                    resin=selected_resin,
                    contaminant=contaminant,
                    initial_toc=initial_toc,
                    ph=ph
                )

                st.subheader("Simulation Results")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Predicted Removal Efficiency", f"{results['predicted_removal_efficiency']:.1%}")
                with col2:
                    st.metric("Final TOC Concentration (mg/L)", f"{results['final_toc_mg_l']:.2f}")
            else:
                st.error("Could not find the selected resin data to run the simulation.")
