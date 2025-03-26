import json
import shutil
import logging
from pathlib import Path 


def check_ext(file_ext: str, category_map: dict, current_path: list = None):
    """
    Busca recursivamente la extensión en el árbol de categorías.
    Retorna: (encontrado, ruta_categoría)
    """

    # Validar entrada
    if not isinstance(category_map, dict):
        raise ValueError("category_map debe ser un diccionario")

    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)

    if current_path is None:
        current_path = []

    # Normalizar extension
    file_ext = file_ext.lower()

    for category, value in category_map.items():
        logging.debug(f'Buscando {file_ext} en {category}')
        new_path = current_path + [category]

        if isinstance(value, dict):
            # Recursion de subcategorias
            found, final_path = check_ext(file_ext, value, new_path)
            if found:
                return True, final_path

        elif isinstance(value, list) and file_ext in value:
            # Extensión encontrada en esta categoría
            logging.info(f'Extension {file_ext} encontrado en {category}')
            return True, new_path

    # No encontrado en ninguna categoría
    logging.warning(f"Extensión {file_ext} no reconocida")
    return False, ['others']


def organizer(directory: Path,
              categories_file: Path,
              output_base: Path = None,
              exclude_patterns: list = None
              ):

    logging.info('Iniciando organizacion')

    # Cargar categorías desde JSON
    logging.debug('Cargando mapa de categorias')
    if not categories_file.exists():
        logging.error(f"Archivo de categorías no encontrado: {categories_file}")
        return
    with open(categories_file) as f:
        categories = json.load(f)
        logging.debug(f'Mapa de categorias {categories_file} cargado con exito')

    # Recorrer archivos en el directorio
    logging.debug(f'Recorriendo archivos en {directory}')
    for file in directory.iterdir():
        logging.debug('Comenzando enrutamiento de archivo')
        file_path = directory / file.name

        # Validar si es archivo
        logging.debug(f'Validando si {file.name} es un archivo')
        if not file_path.is_file():
            logging.warning(f'{file_path} no es un archivo')
            continue

        # Manejar archivos ocultos
        logging.debug(f'Validando si {file.name} es un archivo oculto')
        if file.name.startswith('.'):
            category_path = ['hidden']
        # Manejar archivos sin extension
        elif not file.suffix:
            logging.debug(f'Validando si {file.name} es un archivo sin extension')
            category_path = ['no_extension']
        else:
            # Obtener extensión
            logging.debug('Obteniendo extension de archivo')
            ext = file_path.suffix.lower()
            logging.debug(f'Extension {ext} obtenida')

            # Validar exclusiones
            logging.debug('Validando exclusiones')
            if exclude_patterns and ext in exclude_patterns:
                logging.debug(f'archivo {file.name} en lista de exclusion')
                logging.warning(f'Archivo {file.name} ha sido excluido')
                continue

            found, category_path = check_ext(ext, categories)
            if not found:
                category_path = ['others'] 


        # Construir ruta destino completa
        logging.debug('Creando directorio de destino')
        dest_dir = (output_base or directory).joinpath(*category_path)
        dest_dir.mkdir(parents=True, exist_ok=True)
        logging.debug(f'Directorio {dest_dir} creado exitosamente')

        # Mover archivo
        logging.debug(f'Moviendo archivo {file.name} a {dest_dir}')
        if dest_dir.exists():
            logging.warning(f'Advertencia {dest_dir} ya existe. Sobreescribiendo')
        shutil.move(str(file), str(dest_dir / file.name))
        logging.info(f'Movido: {file_path} -> {dest_dir}')

        logging.info("Organización completada.")
