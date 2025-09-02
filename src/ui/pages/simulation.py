"""
Simulation page for the Resin Simulation application.
"""
from typing import Dict, List
import streamlit as st
from dataclasses import asdict
from ...models import IonFirmware, ComputationalState
from ...core import (
    apply_firmware, 
    run_program, 
    simulate_osmotic_degradation,
    mixed_ion_state
)

def show_simulation_page(base_resin_props: Dict) -> None:
    """
    Display the simulation page.
    
    Args:
        base_resin_props: Dictionary of base resin properties
    """
    st.header("🔬 State Simulation")
    
    mode = st.radio("Mode", ["Single Ion", "Program (Sequence)", "Mixed Form"])
    
    if mode == "Single Ion":
        ion = st.selectbox("Select ion", [i.value for i in IonFirmware if i != IonFirmware.MIXED])
        cycles = st.slider("Degradation Cycles", 0, 1000, 10)
        resin_grade = st.selectbox("Resin Quality", ["premium", "first", "basic"])
        
        if st.button("Run Simulation"):
            ion_enum = IonFirmware(ion)
            state = apply_firmware(None, ion_enum, base_resin_props)
            degraded_state = simulate_osmotic_degradation(state, cycles, resin_grade)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Initial State")
                st.json(asdict(state))
            with col2:
                st.subheader(f"After {cycles} cycles")
                st.json(asdict(degraded_state))
    
    elif mode == "Program (Sequence)":
        program_length = st.number_input("Program Length", 1, 5, 2)
        program = []
        
        for i in range(program_length):
            ion = st.selectbox(
                f"Ion {i+1}",
                [ion.value for ion in IonFirmware if ion != IonFirmware.MIXED],
                key=f"ion_{i}"
            )
            program.append(IonFirmware(ion))
        
        if st.button("Execute Program"):
            final_state = run_program(program, base_resin_props)
            st.subheader("Final State")
            st.json(asdict(final_state))
    
    elif mode == "Mixed Form":
        col1, col2 = st.columns(2)
        with col1:
            ion1 = st.selectbox(
                "Ion 1",
                [ion.value for ion in IonFirmware if ion != IonFirmware.MIXED]
            )
        with col2:
            ion2 = st.selectbox(
                "Ion 2",
                [ion.value for ion in IonFirmware if ion != IonFirmware.MIXED and ion.value != ion1]
            )
        
        fraction = st.slider("Fraction of Ion 1", 0.0, 1.0, 0.5)
        
        if st.button("Mix"):
            mixed = mixed_ion_state(
                IonFirmware(ion1), 
                IonFirmware(ion2), 
                fraction, 
                base_resin_props
            )
            st.subheader("Mixed State")
            st.json(asdict(mixed))
