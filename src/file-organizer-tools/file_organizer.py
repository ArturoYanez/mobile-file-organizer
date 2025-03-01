import json
import shutil
import logging
from pathlib import Path


def check_ext(file_extension, extension_map, category_path=None):
    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)

    # Validar entrada
    if not isinstance(extension_map, dict):
        raise ValueError("extension_map debe ser un diccionario")

    if category_path is None:
        category_path = []

    # Normalizar extensión
    file_extension = file_extension.lower()

    # Buscar extensión en el mapa
    for key, value in extension_map.items():
        logging.debug(f"Buscando {file_extension} en {key}")

        if isinstance(value, list):
            if file_extension in value:
                logging.info(f"Extensión {file_extension} encontrada en {key}")
                return True, category_path + [key]

        elif isinstance(value, dict):
            found, path = check_ext(file_extension, value, category_path + [key])
            if found:
                return found, path

    # Extensión no encontrada
    logging.warning(f"Extensión {file_extension} no reconocida")
    return False, []


def organizer(directory: Path, categories_file: Path):
    # Configurar logging
    logging.basicConfig(level=logging.INFO)

    # Convertir a Path
    base_dir = directory

    # Cargar categorías desde JSON
    c_map = Path(categories_file)
    if not c_map.exists():
        logging.error(f"Archivo de categorías no encontrado: {c_map}")
        return

    with open(c_map) as f:
        categories = json.load(f)

    # Recorrer archivos en el directorio
    for file in base_dir.iterdir():
        file_path = base_dir / file.name

        # Validar si es archivo
        if not file_path.is_file():
            continue

        # Obtener extensión
        ext = file_path.suffix.lower()

        # Buscar categoría
        found, c_path = check_ext(ext, categories)
        if not found:
            logging.warning(f"Ignorado: {file_path} (extensión no reconocida)")
            continue

        # Crear directorio de destino
        n_directory = base_dir
        for folder in c_path:
            n_directory /= folder
        n_directory.mkdir(parents=True, exist_ok=True)

        # Mover archivo (manejar colisiones)
        dest_file = n_directory / file.name
        if dest_file.exists():
            logging.warning(f"Advertencia: {dest_file} ya existe. Sobrescribiendo.")
        shutil.move(file_path, dest_file)
        logging.info(f"Movido: {file_path} -> {dest_file}")

    logging.info("Organización completada.")

