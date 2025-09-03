"""
Tests for the new features added to the application.
"""
import pytest
from src.models.state import Resin
from src.core.simulation import simulate_toc_removal
from src.core.glossary import GLOSSARY_TERMS

def test_load_resin_dataset():
    """
    Tests that the resin dataset can be loaded correctly.
    """
    try:
        resins = Resin.load_from_json('src/core/resin_datasets.json')
        assert isinstance(resins, list)
        assert len(resins) > 0
        assert all(isinstance(r, Resin) for r in resins)
        assert resins[0].name == "CalRes 2304"
    except Exception as e:
        pytest.fail(f"Failed to load or parse resin_datasets.json: {e}")

def test_glossary_loading():
    """
    Tests that the glossary terms can be loaded.
    """
    assert isinstance(GLOSSARY_TERMS, dict)
    assert len(GLOSSARY_TERMS) > 10 # Check for a reasonable number of terms
    assert "Anion Exchange" in GLOSSARY_TERMS

def test_toc_removal_simulation():
    """
    Tests the basic logic of the TOC removal simulation.
    """
    # Find a macroporous resin for the test
    resins = Resin.load_from_json('src/core/resin_datasets.json')
    test_resin = next((r for r in resins if r.structure == "Macroporous"), None)

    assert test_resin is not None, "Test requires at least one macroporous resin in the dataset."

    # Test case 1: Standard conditions
    results = simulate_toc_removal(
        resin=test_resin,
        contaminant="Tannic Acid",
        initial_toc=10.0,
        ph=7.0
    )
    assert "predicted_removal_efficiency" in results
    assert "final_toc_mg_l" in results
    assert 0 < results["predicted_removal_efficiency"] < 1
    assert results["final_toc_mg_l"] < 10.0

    # Test case 2: High pH should reduce efficiency
    results_high_ph = simulate_toc_removal(
        resin=test_resin,
        contaminant="Tannic Acid",
        initial_toc=10.0,
        ph=9.0
    )
    assert results_high_ph["predicted_removal_efficiency"] < results["predicted_removal_efficiency"]
