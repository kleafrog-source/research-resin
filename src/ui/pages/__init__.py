"""
UI pages for the Resin Simulation application.
"""

# Import all page modules here
from .data_view import show_data_view
from .simulation import show_simulation_page
from .analysis import show_analysis_page
from .import_export import show_import_export_page

__all__ = [
    'show_data_view',
    'show_simulation_page',
    'show_analysis_page',
    'show_import_export_page'
]
