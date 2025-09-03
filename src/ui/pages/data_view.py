"""
Data view page for the Resin Simulation application.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from ...models import ComputationalState, IonFirmware, Resin
from ...core.simulation import generate_single_ion_states

def show_data_view(base_resin_props: Dict[str, Any], 
                  single_ion_states: Optional[Dict[IonFirmware, ComputationalState]] = None) -> None:
    """
    Display the data and parameters view.
    
    Args:
        base_resin_props: Dictionary of base resin properties (can be deprecated or used for default simulation)
        single_ion_states: Dictionary mapping ions to their states.
    """
    st.header("📊 Resin Datasets and Properties")
    
    # Load resin data from JSON
    try:
        resins = Resin.load_from_json('src/core/resin_datasets.json')
        resin_names = [r.name for r in resins]
    except Exception as e:
        st.error(f"Error loading resin datasets: {e}")
        return

    # Resin selection
    selected_resin_name = st.selectbox("Select a Resin to View Its Properties", resin_names)
    selected_resin = next((r for r in resins if r.name == selected_resin_name), None)

    if selected_resin:
        st.subheader(f"Properties for {selected_resin.name}")
        
        # Display properties in a more organized way
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Manufacturer", selected_resin.manufacturer)
            st.metric("Type", selected_resin.type)
            st.metric("Structure", selected_resin.structure)
            st.metric("Functional Group", selected_resin.functional_group)
            st.metric("Ionic Form", selected_resin.ionic_form)
        
        with col2:
            st.metric("Max Temperature (°C)", f"{selected_resin.max_temp_c}")
            st.metric("Mean Diameter (μm)", f"{selected_resin.mean_diameter_um}")
            st.metric("Uniformity Coefficient", f"{selected_resin.uniformity_coefficient}")
            if selected_resin.mercury_capacity_g_dm3:
                st.metric("Mercury Capacity (g/dm³)", f"{selected_resin.mercury_capacity_g_dm3}")

        # Display properties with ranges in a table
        st.write("#### Physical & Chemical Properties")
        prop_data = {
            "Property": [
                "Anion Exchange Capacity (min, meq/ml)",
                "Anion Exchange Capacity (max, meq/ml)",
                "Specific Volume (g/ml)",
                "Water Retention Capacity (%)"
            ],
            "Value": [
                selected_resin.anion_exchange_capacity_min_meq_ml,
                selected_resin.anion_exchange_capacity_max_meq_ml,
                selected_resin.specific_volume_g_ml,
                selected_resin.water_retention_capacity_percent
            ]
        }
        prop_df = pd.DataFrame(prop_data)
        st.dataframe(prop_df, hide_index=True, use_container_width=True)

    # The single ion states display can remain as it is, as it shows simulation output
    st.subheader("Simulated Single Ion States")
    if not single_ion_states:
        st.warning("Simulated ion state data is not available.")
    else:
        try:
            single_df_data = []
            for ion, state in single_ion_states.items():
                if state:
                    single_df_data.append({
                        'Ion': ion.value,
                        'Conductivity': f"{state.conductivity:.3e}",
                        'Catalytic Activity': f"{state.catalytic_activity:.3f}",
                        'Structural Role': f"{state.structural_role:.3f}",
                    })

            if single_df_data:
                single_df = pd.DataFrame(single_df_data)
                st.dataframe(single_df, hide_index=True, use_container_width=True)
            else:
                st.warning("No ion state data to display.")
                
        except Exception as e:
            st.error(f"Error displaying ion states: {str(e)}")

# For backward compatibility
show_page = show_data_view
