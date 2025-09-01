"""
Data view page for the Resin Simulation application.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from ...models import ComputationalState, IonFirmware
from ...core.simulation import generate_single_ion_states

def show_data_view(base_resin_props: Dict[str, Any], 
                  single_ion_states: Optional[Dict[IonFirmware, ComputationalState]] = None) -> None:
    """
    Display the data and parameters view.
    
    Args:
        base_resin_props: Dictionary of base resin properties
        single_ion_states: Dictionary mapping ions to their states. If None, will be generated.
    """
    st.header(" Базовые Параметры и Просчитанные Данные")
    
    # Display resin properties
    st.subheader("Параметры Смолы")
    if not base_resin_props:
        st.error("Ошибка: Не загружены параметры смолы")
        return
    
    try:
        # Try to generate ion states if not provided
        if single_ion_states is None:
            with st.spinner("Генерация состояний ионов..."):
                single_ion_states = generate_single_ion_states(base_resin_props)
        
        # Display resin properties in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Параметры Смолы")
            try:
                resin_df = pd.DataFrame(list(base_resin_props.items()), 
                                     columns=['Параметр', 'Значение'])
                st.dataframe(resin_df, hide_index=True, use_container_width=True)
            except Exception as e:
                st.error(f"Ошибка при отображении параметров смолы: {str(e)}")
        
        with col2:
            st.subheader("Диапазоны Свойств")
            try:
                ranges_df = pd.DataFrame({
                    'Свойство': ['Проводимость', 'Каталитическая активность', 'Структурная роль',
                               'Тепловыделение', 'Трение', 'Оптическое качество'],
                    'Мин': [4.200e-02, 0.10, 0.5, -4660, 0.03, 0.35],
                    'Макс': [3.623e-01, 0.90, 0.9, -1090, 0.15, 0.90],
                    'Отношение': [8.6, 9.0, 1.8, 4.3, 5.0, 2.6]
                })
                st.dataframe(ranges_df, hide_index=True, use_container_width=True)
            except Exception as e:
                st.error(f"Ошибка при отображении диапазонов свойств: {str(e)}")
        
        # Display single ion states
        st.subheader("Состояния Одиночных Ионов")
        if not single_ion_states:
            st.warning("Не удалось загрузить данные о состояниях ионов.")
        else:
            try:
                single_df_data = []
                for ion, state in single_ion_states.items():
                    if state:  # Only process valid states
                        single_df_data.append({
                            'Ион': ion.value,
                            'Проводимость': f"{state.conductivity:.3e}",
                            'Каталитическая активность': f"{state.catalytic_activity:.3f}",
                            'Структурная роль': f"{state.structural_role:.3f}",
                            'Тепловыделение': f"{state.thermal_power:.1f}",
                            'Трение': f"{state.tribological_performance:.3f}",
                            'Оптическое качество': f"{state.optical_quality:.3f}"
                        })
                
                if single_df_data:
                    single_df = pd.DataFrame(single_df_data)
                    st.dataframe(single_df, hide_index=True, use_container_width=True)
                else:
                    st.warning("Нет данных о состояниях ионов для отображения.")
                    
            except Exception as e:
                st.error(f"Ошибка при отображении состояний ионов: {str(e)}")
                
    except Exception as e:
        st.error(f"Критическая ошибка: {str(e)}")
        st.exception(e)  # Show detailed traceback

# For backward compatibility
show_page = show_data_view
