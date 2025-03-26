# test_file_organizer.py
import pytest
import sys
import json
from pathlib import Path
from unittest.mock import patch

# Añade el directorio src al path de Python
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from file_organizer_tools.file_organizer import organizer

def write_categories(tmp_path, categories):
    categories_file = tmp_path / "categories.json"
    with open(categories_file, 'w') as f:
        json.dump(categories, f)
    return categories_file

def test_hidden_files(tmp_path):
    # Configurar
    source = tmp_path / "source"
    source.mkdir()
    hidden_file = source / ".gitignore"
    hidden_file.touch()
    
    output = tmp_path / "output"
    
    # Crear archivo de categorías
    categories = {
        "docs": [".pdf", ".txt"],
        "images": [".png", ".jpg"],
        "others": []
    }
    categories_file = write_categories(tmp_path, categories)
    
    # Ejecutar
    organizer(directory=source, categories_file=categories_file, output_base=output)
    
    # Verificar
    assert (output / "hidden/.gitignore").exists()

def test_no_extension_files(tmp_path):
    # Configurar
    source = tmp_path / "source"
    source.mkdir()
    no_ext_file = source / "README"
    no_ext_file.touch()
    
    output = tmp_path / "output"
    
    # Crear archivo de categorías
    categories = {
        "docs": [".pdf", ".txt"],
        "images": [".png", ".jpg"],
        "others": []
    }
    categories_file = write_categories(tmp_path, categories)
    
    # Ejecutar
    organizer(directory=source, categories_file=categories_file, output_base=output)
    
    # Verificar
    assert (output / "no_extension/README").exists()

def test_default_category_mapping(tmp_path):
    # Testear mapeo por defecto de categorías
    source = tmp_path / "source"
    source.mkdir()
    test_files = {
        'image.png': 'images',
        'doc.pdf': 'docs',
        'unknown.xyz': 'others'
    }
    
    for f, cat in test_files.items():
        (source / f).touch()
    
    output = tmp_path / "output"
    
    # Crear archivo de categorías
    categories = {
        "docs": [".pdf", ".txt"],
        "images": [".png", ".jpg"],
        "others": []
    }
    categories_file = write_categories(tmp_path, categories)
    
    organizer(directory=source, categories_file=categories_file, output_base=output)
    
    for f, cat in test_files.items():
        assert (output / cat / f).exists()
