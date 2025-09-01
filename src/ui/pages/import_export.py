"""
Import/Export page for the Resin Simulation application.
"""
import json
import io
import pandas as pd
from typing import Dict, Any, Optional
import streamlit as st
from ...models import ComputationalState, IonFirmware

class ResinDataExporter:
    """Handles exporting resin data to different formats."""
    
    @staticmethod
    def to_json(data: Dict[str, Any]) -> str:
        """Convert data to JSON string."""
        return json.dumps(data, indent=4, ensure_ascii=False)
    
    @staticmethod
    def to_csv(data: Dict[IonFirmware, ComputationalState]) -> str:
        """Convert ion states to CSV format."""
        rows = []
        for ion, state in data.items():
            row = {'ion': ion.value}
            row.update(state.to_dict())
            rows.append(row)
        
        df = pd.DataFrame(rows)
        return df.to_csv(index=False)


class ResinDataImporter:
    """Handles importing resin data from different formats."""
    
    @staticmethod
    def from_json(file_content: str) -> Dict[str, Any]:
        """Import data from JSON string."""
        try:
            return json.loads(file_content)
        except json.JSONDecodeError as e:
            st.error(f"Ошибка при чтении JSON: {e}")
            return {}
    
    @staticmethod
    def from_csv(file_content: str) -> pd.DataFrame:
        """Import data from CSV string."""
        try:
            return pd.read_csv(io.StringIO(file_content))
        except Exception as e:
            st.error(f"Ошибка при чтении CSV: {e}")
            return pd.DataFrame()


def show_import_export_page(
    base_resin_props: Dict[str, Any],
    single_ion_states: Dict[IonFirmware, ComputationalState]
) -> None:
    """
    Display the import/export page.
    
    Args:
        base_resin_props: Dictionary of base resin properties
        single_ion_states: Dictionary mapping ions to their states
    """
    st.header("🔄 Импорт/Экспорт Данных")
    
    format_type = st.selectbox("Формат", ["JSON", "CSV"])
    
    if format_type == "JSON":
        # Prepare data for export
        data_to_export = {
            "base_resin_props": base_resin_props,
            "single_ion_states": {
                ion.value: state.to_dict() 
                for ion, state in single_ion_states.items()
            }
        }
        
        # Export JSON
        json_str = ResinDataExporter.to_json(data_to_export)
        
        st.download_button(
            label="Экспорт JSON",
            data=json_str,
            file_name="resin_data.json",
            mime="application/json"
        )
        
        # Import JSON
        uploaded_file = st.file_uploader(
            "Импорт JSON", 
            type="json",
            key="json_uploader"
        )
        
        if uploaded_file is not None:
            try:
                imported_data = ResinDataImporter.from_json(
                    uploaded_file.getvalue().decode()
                )
                st.success("Данные успешно загружены!")
                st.json(imported_data)
            except Exception as e:
                st.error(f"Ошибка при загрузке файла: {e}")
    
    elif format_type == "CSV":
        # Export CSV
        csv_data = ResinDataExporter.to_csv(single_ion_states)
        
        st.download_button(
            label="Экспорт CSV (Состояния ионов)",
            data=csv_data,
            file_name="ion_states.csv",
            mime="text/csv"
        )
        
        # Import CSV
        uploaded_file = st.file_uploader(
            "Импорт CSV", 
            type="csv",
            key="csv_uploader"
        )
        
        if uploaded_file is not None:
            try:
                df = ResinDataImporter.from_csv(
                    uploaded_file.getvalue().decode()
                )
                if not df.empty:
                    st.success("Данные успешно загружены!")
                    st.dataframe(df)
            except Exception as e:
                st.error(f"Ошибка при загрузке файла: {e}")
