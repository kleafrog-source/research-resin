"""
This module defines the Glossary page for the Streamlit application.
"""
import streamlit as st
from ...core.glossary import GLOSSARY_TERMS

def show_glossary_page():
    """
    Displays the glossary of terms.
    """
    st.header("📖 Glossary of Terms")
    st.markdown("A collection of important terms and definitions related to ion-exchange resins.")

    # Sort terms alphabetically for easy navigation
    sorted_terms = sorted(GLOSSARY_TERMS.items())

    for term, definition in sorted_terms:
        with st.expander(term):
            st.markdown(definition)
