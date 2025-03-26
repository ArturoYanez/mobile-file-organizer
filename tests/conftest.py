# conftest.py (Configuración global de pytest)
import pytest
from pathlib import Path
from unittest.mock import Mock

@pytest.fixture
def default_categories():
    return {
        'images': ['.png', '.jpg'],
        'docs': ['.pdf', '.txt'],
        'others': []
    }
