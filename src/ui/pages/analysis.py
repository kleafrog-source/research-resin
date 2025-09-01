"""
Analysis and visualization page for the Resin Simulation application.
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from dataclasses import asdict
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

from ...models import IonFirmware, ComputationalState
from ...core import apply_firmware, simulate_osmotic_degradation, generate_single_ion_states

def plot_degradation(states: List[Tuple[int, ComputationalState]], property_name: str) -> None:
    """
    Plot property degradation over cycles.
    
    Args:
        states: List of (cycle, state) tuples
        property_name: Name of the property to plot
    """
    cycles = [cycle for cycle, _ in states]
    values = [getattr(state, property_name) for _, state in states]
    
    plt.figure(figsize=(10, 5))
    plt.plot(cycles, values, 'b-o')
    plt.title(f'Деградация свойства: {property_name}')
    plt.xlabel('Количество циклов')
    plt.ylabel(property_name)
    plt.grid(True)
    st.pyplot(plt)

def show_analysis_page(base_resin_props: Dict) -> None:
    """
    Display the analysis and visualization page.
    
    Args:
        base_resin_props: Dictionary of base resin properties
    """
    st.header("📈 Анализ и Визуализации")
    
    analysis_type = st.selectbox("Тип анализа", ["Кластеризация", "Регрессия", "Деградация"])
    
    if analysis_type == "Кластеризация":
        st.subheader("Кластеризация Состояний Ионов")
        
        # Generate ion states if not in session state
        if 'ion_states' not in st.session_state:
            st.session_state.ion_states = generate_single_ion_states(base_resin_props)
        
        # Prepare data for clustering
        ions = []
        features = []
        
        for ion, state in st.session_state.ion_states.items():
            if state:  # Only process valid states
                ions.append(ion.value)
                features.append([
                    state.conductivity,
                    state.catalytic_activity,
                    state.structural_role,
                    state.thermal_power,
                    state.tribological_performance,
                    state.optical_quality
                ])
        
        if not features:
            st.warning("Нет данных о состояниях ионов для кластеризации.")
            return
        
        # Scale features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        # Let user choose number of clusters
        n_clusters = st.slider("Количество кластеров", 2, min(10, len(ions)), 3)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(scaled_features)
        
        # Create DataFrame for visualization
        df = pd.DataFrame(features, columns=[
            'Проводимость', 'Каталитическая активность', 
            'Структурная роль', 'Тепловыделение',
            'Трение', 'Оптическое качество'
        ])
        df['Ион'] = ions
        df['Кластер'] = cluster_labels
        
        # 3D Scatter plot using plotly
        st.subheader("3D Визуализация Кластеров")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_axis = st.selectbox("Ось X", df.columns[:-2], index=0)
        with col2:
            y_axis = st.selectbox("Ось Y", df.columns[:-2], index=1)
        with col3:
            z_axis = st.selectbox("Ось Z", df.columns[:-2], index=2)
        
        fig = px.scatter_3d(
            df, 
            x=x_axis, 
            y=y_axis, 
            z=z_axis,
            color='Кластер',
            hover_name='Ион',
            title=f'Кластеризация ионов по свойствам',
            labels={
                x_axis: x_axis,
                y_axis: y_axis,
                z_axis: z_axis,
                'Кластер': 'Кластер'
            },
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        # Update marker size and opacity for better visibility
        fig.update_traces(
            marker=dict(size=8, opacity=0.8, line=dict(width=0.5, color='DarkSlateGrey')),
            selector=dict(mode='markers')
        )
        
        # Update layout for better readability
        fig.update_layout(
            scene=dict(
                xaxis_title=x_axis,
                yaxis_title=y_axis,
                zaxis_title=z_axis,
            ),
            margin=dict(l=0, r=0, b=0, t=30),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show cluster centers
        st.subheader("Центры Кластеров")
        cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
        centers_df = pd.DataFrame(
            cluster_centers,
            columns=df.columns[:-2]
        )
        st.dataframe(centers_df, use_container_width=True)
        
        # Show cluster members
        st.subheader("Состав Кластеров")
        for cluster_id in range(n_clusters):
            cluster_members = df[df['Кластер'] == cluster_id]['Ион'].tolist()
            st.write(f"**Кластер {cluster_id + 1}** ({len(cluster_members)} ионов): {', '.join(cluster_members)}")
    
    elif analysis_type == "Регрессия":
        st.subheader("Анализ Регрессии")
        
        # Example regression results (would come from actual analysis)
        regression_results = {
            'conductivity': [('Гидратация', 100.0), ('Энергия', 85.2), 
                           ('Селективность', 42.1), ('Заряд', 15.8)],
            'catalytic_activity': [('Заряд', 100.0), ('Селективность', 78.3), 
                                 ('Энергия', 45.6), ('Гидратация', 22.1)],
            'tribological': [('Энергия', 100.0), ('Заряд', 72.4), 
                           ('Селективность', 38.9), ('Гидратация', 18.5)]
        }
        
        selected_property = st.selectbox(
            "Выберите свойство для анализа",
            list(regression_results.keys())
        )
        
        if selected_property in regression_results:
            df = pd.DataFrame(
                regression_results[selected_property],
                columns=['Фактор', 'Влияние (%)']
            )
            st.dataframe(df, hide_index=True)
            
            # Simple bar chart
            fig, ax = plt.subplots()
            ax.bar(df['Фактор'], df['Влияние (%)'])
            ax.set_ylabel('Влияние (%)')
            ax.set_title(f'Влияние факторов на {selected_property}')
            st.pyplot(fig)
    
    elif analysis_type == "Деградация":
        st.subheader("Симуляция Деградации")
        
        ion = st.selectbox(
            "Выберите ион",
            [i.value for i in IonFirmware if i != IonFirmware.MIXED]
        )
        
        cycles = st.slider("Максимальное количество циклов", 1, 1000, 100)
        step = st.slider("Шаг отображения", 1, 100, 10)
        resin_grade = st.selectbox(
            "Качество смолы", 
            ["высший", "первый", "базовый"]
        )
        
        if st.button("Анализировать"):
            ion_enum = IonFirmware(ion)
            initial_state = apply_firmware(None, ion_enum, base_resin_props)
            
            # Simulate degradation at each step
            states = []
            for cycle in range(0, cycles + 1, step):
                state = simulate_osmotic_degradation(initial_state, cycle, resin_grade)
                states.append((cycle, state))
            
            # Plot different properties
            properties = [
                'conductivity', 'catalytic_activity', 
                'structural_role', 'optical_quality'
            ]
            
            for prop in properties:
                plot_degradation(states, prop)
            
            # Show final state
            st.subheader("Финальное состояние")
            st.json(asdict(states[-1][1]))
