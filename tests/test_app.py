import pytest

def test_app_import():
    """
    Tests that the main application can be imported without raising exceptions.
    """
    try:
        import app
    except ImportError as e:
        pytest.fail(f"Failed to import the application: {e}")

def test_glossary_page_import():
    """
    Tests that the glossary page can be imported.
    """
    try:
        from src.ui.pages import glossary_page
    except ImportError as e:
        pytest.fail(f"Failed to import glossary_page: {e}")

def test_toc_removal_page_import():
    """
    Tests that the TOC removal page can be imported.
    """
    try:
        from src.ui.pages import toc_removal_page
    except ImportError as e:
        pytest.fail(f"Failed to import toc_removal_page: {e}")
