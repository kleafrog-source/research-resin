"""
Advanced analysis and visualization of resin properties.
"""
from typing import Dict, Any, List, Optional
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ...models import IonFirmware, ComputationalState

def show_advanced_analysis(ion_states: Dict[IonFirmware, ComputationalState]):
    """Display advanced analysis interface."""
    st.header("📈 Advanced Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Correlation Matrix", "Property Trends", "Ion Comparison", "Property Distribution"]
    )
    
    if analysis_type == "Correlation Matrix":
        _show_correlation_analysis(ion_states)
    elif analysis_type == "Property Trends":
        _show_property_trends(ion_states)
    elif analysis_type == "Ion Comparison":
        _show_ion_comparison(ion_states)
    elif analysis_type == "Property Distribution":
        _show_property_distribution(ion_states)

def _show_correlation_analysis(ion_states: Dict[IonFirmware, ComputationalState]):
    """Display correlation matrix of resin properties."""
    st.subheader("Property Correlation Matrix")
    
    # Prepare data for correlation matrix
    data = []
    for ion, state in ion_states.items():
        if hasattr(ion, 'value'):
            ion_name = ion.value
        else:
            ion_name = str(ion)
            
        row = {
            "Ion": ion_name,
            "Charge": getattr(state, 'charge', 0),
            "Ionic Radius": getattr(state, 'ionic_radius', 0),
            "Hydration Energy": getattr(state, 'hydration_energy', 0),
            "Electronegativity": getattr(state, 'electronegativity', 0),
            "Polarizability": getattr(state, 'polarizability', 0)
        }
        
        # Add other properties if they exist
        for prop in ['conductivity', 'catalytic_activity', 'swelling_ratio',
                    'mechanical_strength', 'ion_diffusion_rate', 'selectivity_coefficient',
                    'chemical_stability', 'optical_quality', 'surface_area']:
            row[prop] = getattr(state, prop, 0)
            
        data.append(row)
    
    df = pd.DataFrame(data).set_index("Ion")
    
    # Calculate correlation matrix
    corr = df.corr()
    
    # Create heatmap
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu',
        zmin=-1,
        zmax=1,
        title='Correlation Between Resin Properties'
    )
    
    fig.update_layout(height=700)
    st.plotly_chart(fig, use_container_width=True)
    
    # Show strong correlations
    strong_corrs = []
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            val = corr.iloc[i, j]
            if abs(val) > 0.7:  # Threshold for strong correlation
                strong_corrs.append((corr.columns[i], corr.columns[j], val))
    
    if strong_corrs:
        st.subheader("Strong Correlations")
        for prop1, prop2, corr_val in strong_corrs:
            st.write(f"- **{prop1}** and **{prop2}**: {corr_val:.2f}")

def _show_property_trends(ion_states: Dict[IonFirmware, ComputationalState]):
    """Display trends of properties across different ion types."""
    st.subheader("Property Trends")
    
    # Group ions by charge
    ion_groups = {
        "1+": [IonFirmware.H_PLUS, IonFirmware.NA_PLUS, IonFirmware.K_PLUS],
        "2+": [IonFirmware.CA_2PLUS, IonFirmware.MG_2PLUS, IonFirmware.CU_2PLUS, IonFirmware.ZN_2PLUS],
        "3+": [IonFirmware.FE_3PLUS, IonFirmware.AL_3PLUS]
    }
    
    # Get available properties from the first ion state
    if not ion_states:
        st.warning("No ion states available for analysis.")
        return
    
    sample_state = next(iter(ion_states.values()))
    available_props = [
        prop for prop in dir(sample_state) 
        if not prop.startswith('_') and not callable(getattr(sample_state, prop))
    ]
    
    # Property selection
    selected_props = st.multiselect(
        "Select Properties to Compare",
        available_props,
        default=["conductivity", "mechanical_strength", "swelling_ratio"],
        max_selections=5
    )
    
    if not selected_props:
        st.warning("Please select at least one property.")
        return
    
    # Create a plot for each property
    for prop in selected_props:
        fig = go.Figure()
        
        for charge, ions in ion_groups.items():
            x_vals = [ion.value for ion in ions if ion in ion_states]
            y_vals = [getattr(ion_states[ion], prop) for ion in ions if ion in ion_states]
            
            if x_vals:
                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines+markers',
                    name=f'{charge} charge',
                    line=dict(width=2)
                ))
        
        fig.update_layout(
            title=f"{prop.replace('_', ' ').title()} by Ion Type",
            xaxis_title="Ion",
            yaxis_title=prop.replace('_', ' ').title(),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def _show_ion_comparison(ion_states: Dict[IonFirmware, ComputationalState]):
    """Compare properties of selected ions."""
    st.subheader("Ion Comparison")
    
    if not ion_states:
        st.warning("No ion states available for comparison.")
        return
    
    # Get available ions and properties
    available_ions = [ion.value for ion in ion_states.keys()]
    selected_ions = st.multiselect(
        "Select Ions to Compare",
        available_ions,
        default=available_ions[:3] if len(available_ions) > 2 else available_ions
    )
    
    if not selected_ions:
        st.warning("Please select at least one ion.")
        return
    
    # Get available properties from the first ion
    sample_state = next(iter(ion_states.values()))
    available_props = [
        prop for prop in dir(sample_state) 
        if not prop.startswith('_') and not callable(getattr(sample_state, prop))
    ]
    
    selected_props = st.multiselect(
        "Select Properties to Compare",
        available_props,
        default=available_props[:5],
        max_selections=10
    )
    
    if not selected_props:
        st.warning("Please select at least one property.")
        return
    
    # Create radar chart for comparison
    fig = go.Figure()
    
    for ion_name in selected_ions:
        ion = next((k for k, v in ion_states.items() if v == ion_name), None)
        if ion:
            values = [getattr(ion_states[ion], prop) for prop in selected_props]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=selected_props,
                fill='toself',
                name=ion_name
            ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Ion Property Comparison",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

def _show_property_distribution(ion_states: Dict[IonFirmware, ComputationalState]):
    """Show distribution of properties across all ions."""
    st.subheader("Property Distribution")
    
    if not ion_states:
        st.warning("No ion states available for analysis.")
        return
    
    # Get available properties from the first ion
    sample_state = next(iter(ion_states.values()))
    available_props = [
        prop for prop in dir(sample_state) 
        if not prop.startswith('_') and not callable(getattr(sample_state, prop))
    ]
    
    selected_prop = st.selectbox("Select Property", available_props)
    
    # Create histogram
    values = [getattr(state, selected_prop) for state in ion_states.values()]
    
    if not values:
        st.warning("No data available for the selected property.")
        return
    
    fig = px.histogram(
        x=values,
        nbins=10,
        title=f"Distribution of {selected_prop.replace('_', ' ').title()}",
        labels={'x': selected_prop.replace('_', ' ').title()}
    )
    
    # Add statistics
    stats = {
        "Mean": np.mean(values),
        "Median": np.median(values),
        "Std Dev": np.std(values),
        "Min": min(values),
        "Max": max(values)
    }
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display statistics
    st.subheader("Statistics")
    cols = st.columns(len(stats))
    for (name, value), col in zip(stats.items(), cols):
        with col:
            st.metric(name, f"{value:.4f}")
