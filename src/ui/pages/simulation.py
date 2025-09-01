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
    st.header("🔬 Симуляция Состояний")
    
    mode = st.radio("Режим", ["Одиночный Ион", "Программа (Последовательность)", "Смешанная Форма"])
    
    if mode == "Одиночный Ион":
        ion = st.selectbox("Выберите ион", [i.value for i in IonFirmware if i != IonFirmware.MIXED])
        cycles = st.slider("Циклы деградации", 0, 1000, 10)
        resin_grade = st.selectbox("Качество смолы", ["высший", "первый", "базовый"])
        
        if st.button("Запустить симуляцию"):
            ion_enum = IonFirmware(ion)
            state = apply_firmware(None, ion_enum, base_resin_props)
            degraded_state = simulate_osmotic_degradation(state, cycles, resin_grade)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Исходное состояние")
                st.json(asdict(state))
            with col2:
                st.subheader(f"После {cycles} циклов")
                st.json(asdict(degraded_state))
    
    elif mode == "Программа (Последовательность)":
        program_length = st.number_input("Длина программы", 1, 5, 2)
        program = []
        
        for i in range(program_length):
            ion = st.selectbox(
                f"Ион {i+1}",
                [ion.value for ion in IonFirmware if ion != IonFirmware.MIXED],
                key=f"ion_{i}"
            )
            program.append(IonFirmware(ion))
        
        if st.button("Выполнить программу"):
            final_state = run_program(program, base_resin_props)
            st.subheader("Финальное состояние")
            st.json(asdict(final_state))
    
    elif mode == "Смешанная Форма":
        col1, col2 = st.columns(2)
        with col1:
            ion1 = st.selectbox(
                "Ион 1",
                [ion.value for ion in IonFirmware if ion != IonFirmware.MIXED]
            )
        with col2:
            ion2 = st.selectbox(
                "Ион 2",
                [ion.value for ion in IonFirmware if ion != IonFirmware.MIXED and ion.value != ion1]
            )
        
        fraction = st.slider("Доля Иона 1", 0.0, 1.0, 0.5)
        
        if st.button("Смешать"):
            mixed = mixed_ion_state(
                IonFirmware(ion1), 
                IonFirmware(ion2), 
                fraction, 
                base_resin_props
            )
            st.subheader("Смешанное состояние")
            st.json(asdict(mixed))
