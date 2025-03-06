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


def organizer(directory: Path, categories_file: Path, exclude_patter=[]):
    logging.info('Iniciando organizacion')

    # Cargar categorías desde JSON
    logging.debug('Cargando mapa de categorias')
    c_map = Path(categories_file)
    if not c_map.exists():
        logging.error(f"Archivo de categorías no encontrado: {c_map}")
        return
    with open(c_map) as f:
        categories = json.load(f)
        logging.debug(f'Mapa de categorias {c_map} cargado con exito')

    # Recorrer archivos en el directorio
    logging.debug(f'Recorriendo archivos en {directory}')
    for file in directory.iterdir():
        logging.debug('Enrutamiento de archivo')
        file_path = directory / file.name

        # Validar si es archivo
        if not file_path.is_file():
            logging.warning(f'{file_path} no es un archivo')
            continue

        # Obtener extensión
        logging.debug('Obteniendo eztension de archivo')
        ext = file_path.suffix.lower()
        logging.debug(f'Extension {ext} obtenida')

        # Validar exclusiones
        logging.debug('Validando exclusiones')
        if ext in exclude_patter:
            logging.debug(f'archivo {file.name} en lista de exclusion')
            logging.warning(f'Archivo {file.name} ha sido excluido')
            continue

        # Buscar categoría
        logging.debug('Buscando categoria')
        found, c_path = check_ext(ext, categories)
        if not found:
            logging.warning(f"Ignorado: {file_path} (extensión no reconocida)")
            continue

        # Crear directorio de destino
        logging.debug('Creando directorio de destino')
        n_directory = directory
        for folder in c_path:
            n_directory /= folder
        n_directory.mkdir(parents=True, exist_ok=True)
        logging.debug(f'Directorio {c_path} creado exitosamente')

        # Mover archivo (manejar colisiones)
        logging.debug('Moviendo archivo a directorio destino')
        dest_file = n_directory / file.name
        if dest_file.exists():
            logging.warning(f"Advertencia: {dest_file} ya existe. Sobrescribiendo.")
        shutil.move(file_path, dest_file)
        logging.info(f"Movido: {file_path} -> {dest_file}")

    logging.info("Organización completada.")
