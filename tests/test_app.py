import pytest

def test_app_import():
    """
    Tests that the main application can be imported without raising exceptions.
    """
    try:
        import app
    except ImportError as e:
        pytest.fail(f"Failed to import the application: {e}")
