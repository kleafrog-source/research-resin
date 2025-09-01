"""
Prediction interface for estimating resin properties of new ions.
"""
from typing import Dict, Any, Optional
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from ...models import IonFirmware
from ...core.prediction import PropertyPredictor

def show_prediction_interface(predictor: PropertyPredictor):
    """Display the prediction interface."""
    st.header("🔮 Property Prediction for New Ions")
    
    st.markdown("""
    This tool predicts resin properties for new ions based on their physical characteristics.
    Adjust the sliders to define the ion's properties and see the predicted effects on the resin.
    """)
    
    # Create input columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ion Properties")
        charge = st.slider(
            "Charge", 
            min_value=1, 
            max_value=4, 
            value=1,
            help="Ionic charge (e.g., 1 for Na+, 2 for Ca2+)"
        )
        
        radius = st.slider(
            "Ionic Radius (nm)", 
            min_value=0.2, 
            max_value=0.8, 
            value=0.3, 
            step=0.01,
            help="Effective ionic radius in nanometers"
        )
        
        hydration_energy = st.slider(
            "Hydration Energy (kJ/mol)", 
            min_value=0, 
            max_value=5000, 
            value=1000, 
            step=10,
            help="Energy released when ion is hydrated"
        )
    
    with col2:
        st.subheader("Chemical Properties")
        
        electronegativity = st.slider(
            "Electronegativity (Pauling scale)", 
            min_value=0.5, 
            max_value=3.5, 
            value=1.5, 
            step=0.1,
            help="Pauling electronegativity"
        )
        
        hydration_number = st.slider(
            "Hydration Number", 
            min_value=1, 
            max_value=12, 
            value=6,
            help="Number of water molecules in primary hydration shell"
        )
        
        polarizability = st.slider(
            "Polarizability", 
            min_value=0.1, 
            max_value=10.0, 
            value=1.0, 
            step=0.1,
            help="Polarizability of the ion"
        )
    
    # Make predictions
    if st.button("Predict Properties", type="primary"):
        with st.spinner("Calculating predictions..."):
            try:
                predictions = predictor.predict_for_new_ion(
                    charge=charge,
                    radius=radius,
                    hydration_energy=hydration_energy,
                    electronegativity=electronegativity,
                    hydration_number=hydration_number
                )
                
                if not predictions:
                    st.warning("No predictions available. Please train the models first.")
                    return
                
                # Display predictions
                st.subheader("Predicted Properties")
                
                # Group properties into categories for better organization
                property_groups = {
                    "Electrical Properties": ["conductivity", "ion_diffusion_rate"],
                    "Mechanical Properties": ["mechanical_strength", "swelling_ratio"],
                    "Chemical Properties": ["catalytic_activity", "chemical_stability", "selectivity_coefficient"],
                    "Physical Properties": ["optical_quality", "surface_area"]
                }
                
                # Create columns for metrics
                for group_name, props in property_groups.items():
                    st.markdown(f"### {group_name}")
                    cols = st.columns(len(props))
                    
                    for i, prop in enumerate(props):
                        if prop in predictions:
                            with cols[i]:
                                st.metric(
                                    label=prop.replace("_", " ").title(),
                                    value=f"{predictions[prop]:.4f}"
                                )
                
                # Show feature importances
                st.subheader("Feature Importances")
                
                # Let user select which property's feature importances to view
                selected_prop = st.selectbox(
                    "Select property to view feature importances",
                    list(predictions.keys())
                )
                
                if selected_prop in predictor.models:
                    importances = predictor.get_feature_importances(selected_prop)
                    
                    if importances:
                        # Create a bar chart of feature importances
                        fig = px.bar(
                            x=list(importances.keys()),
                            y=list(importances.values()),
                            labels={'x': 'Feature', 'y': 'Importance'},
                            title=f"Feature Importances for {selected_prop.replace('_', ' ').title()}"
                        )
                        
                        fig.update_layout(
                            xaxis_title="Feature",
                            yaxis_title="Importance",
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display importance values in a table
                        st.write("### Feature Importance Values")
                        importance_df = pd.DataFrame(
                            importances.items(),
                            columns=["Feature", "Importance"]
                        ).sort_values("Importance", ascending=False)
                        
                        st.dataframe(
                            importance_df,
                            column_config={
                                "Feature": "Feature",
                                "Importance": st.column_config.ProgressColumn(
                                    "Importance",
                                    format="%.3f",
                                    min_value=0,
                                    max_value=1.0
                                )
                            },
                            use_container_width=True
                        )
                
                # Provide interpretation of results
                st.subheader("Interpretation")
                
                with st.expander("How to interpret these results"):
                    st.markdown("""
                    - **Conductivity**: Higher values indicate better electrical conductivity
                    - **Ion Diffusion Rate**: How quickly ions move through the resin
                    - **Mechanical Strength**: Resistance to deformation (higher is stronger)
                    - **Swelling Ratio**: Volume change (1.0 = no change, >1.0 = expansion, <1.0 = contraction)
                    - **Catalytic Activity**: Ability to catalyze reactions
                    - **Chemical Stability**: Resistance to chemical degradation (higher is more stable)
                    - **Selectivity Coefficient**: Preference for specific ions
                    - **Optical Quality**: Clarity/transparency of the resin
                    - **Surface Area**: Available surface area for reactions
                    """)
                
            except Exception as e:
                st.error(f"Error generating predictions: {str(e)}")
                st.exception(e)
