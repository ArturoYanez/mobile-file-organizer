from configparser import ConfigParser
import logging
import argparse
import json
from pathlib import Path
import file_organizer as fo
import backup_manager as bm
import password_validator as pv

# Set Configs Routes and Files
CONFIG_DIR = Path.home() / '.config' / 'mt_triad'
CONFIG_FILE = CONFIG_DIR / 'mt_triad.ini'
CATEGORIES_FILE = CONFIG_DIR / 'categories.json'

# Rutas de archuivos por defecto (Desareollo)
DEV_DATA_DIR = Path(__file__).resolve().parent / 'data'
DEFAULT_COKFIG_FILE = DEV_DATA_DIR / 'default.ini'
DEFAULT_CATEGORIES_MAP = DEV_DATA_DIR / 'categories.json'

def setup_logs():
    # Leer configuraciones
    config = ConfigParser()
    config.read(CONFIG_FILE)

    # Configurar logging
    log_level_str = config.get("GLOBAL", "log_level").upper()

    # Mapeo de niveles paea el log
    log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR":logging.ERROR,
            "CRITICAL": logging.CRITICAL
            }
    log_level = log_levels.get(log_level_str, logging.INFO)
    logging.basicConfig(level=log_level, format="[%(levelname)s] %(message)s")

    logging.debug(f'Archivo de configuracion leido de {CONFIG_FILE}')
    print(f"Nivel de log efectivo: {logging.root.level}") # Agregar esta línea
    for handler in logging.root.handlers: # Agregar este bucle
        print(f"Handler: {handler}, Level: {handler.level}")
    logging.debug(f'LOG LEVEL estsblecido correctamente como {log_level}')

def load_default_categories():
    # Carga archico de categorias por defecto
    try:
        with open(DEFAULT_CATEGORIES_MAP) as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error cargando categorías por defecto: {e}")
        return {}

def load_default_configs():
    from configparser import ConfigParser

    try:
        config = ConfigParser()
        config.read(DEFAULT_COKFIG_FILE)
        return config
    except Exception as e:
        logging.error(f'Error cargando configuracion por defecto {e}')
        return ConfigParser()

def load_configs():
    """Crea archivos de configuración si no existen."""
    # Crear directorio de configuraciones
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    logging.debug(f'Directorio de configuraciones creado en {CONFIG_DIR}')

    # Crear archivo de configuraciones por defecto
    if not CONFIG_FILE.exists():
        default_config = load_default_configs()
        with open(CONFIG_FILE, 'w') as f:
            default_config.write(f)
        logging.debug(f'Archivo de configuración {CONFIG_FILE} creado.')

    # Crear mapa de categorías por defecto
    if not CATEGORIES_FILE.exists():
        default_categories = load_default_categories()
        with open(CATEGORIES_FILE, "w") as f:
            json.dump(default_categories, f, indent=4)
        logging.debug(f'Mapa de categorías creado en {CATEGORIES_FILE}')

def main():
    #Cargar configuraciones
    load_configs()

    # Configurar CLI Arguments
    parser = argparse.ArgumentParser(
        description='Paquete de herramientas para gestión de archivos empresariales. '
                    'Organizar archivos de directorios concretos por extensión, '
                    'validar seguridad de contraseñas en ficheros CSV por criterios, '
                    'y crear copias de seguridad en archivos ZIP locales.'
    )
    parser.add_argument('-o', metavar='RUTA_DIRECTORIO', help='Organizar archivos')
    parser.add_argument('-p', metavar='RUTA_ARCHIVO', help='Validar contraseñas de archivo CSV')
    parser.add_argument('-b', metavar='RUTA_DIRECTORIO', help='Realizar Backup de ficheros en ZIP')

    args = parser.parse_args()

    # Ejecutar funcionalidad
    if args.o:
        directory_path = Path(Path.home() / args.o)
        if not directory_path.exists():
            logging.error(f"Directorio no encontrado: {directory_path}")
            return
        fo.organizer(directory_path, categories_file=CATEGORIES_FILE)

    elif args.b:
        directory_path = Path(args.b)
        if not directory_path.exists():
            logging.error(f"Directorio no encontrado: {directory_path}")
            return
        bm.create_backup(directory_path)

    elif args.p:
        file_path = Path(args.p)
        if not file_path.exists():
            logging.error(f"Archivo no encontrado: {file_path}")
            return
        pv.get_data(file_path)

if __name__ == '__main__':
    setup_logs()
    main()
