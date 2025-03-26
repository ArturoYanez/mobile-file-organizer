import os
import platform
import logging
import json
from configparser import ConfigParser
from pathlib import Path

def en_termux():
    return 'TERMUX_VERSION' in os.environ

def obtener_sistema_operativo():
    """
    Obtiene el nombre del sistema operativo.

    Returns:
        str: Nombre del sistema operativo (Windows, Linux, Darwin, Java u otro).
    """

    nombre_os = os.name
    
    if en_termux():
        return 'Termux'
        # os.makedirs('/data/data/com.termux/files/home/.config/mt_triad/')
        # print('Fichero creado correctamente')
    if nombre_os == 'nt':
        return 'Windows'
    elif nombre_os == 'posix':
        sistema = platform.system()
        if sistema == 'Linux':
            return 'Linux'
        elif sistema == 'Darwin':
            return 'macOS'
        elif sistema == 'Android':
            return 'Android'
        else:
            return sistema  # Otros sistemas POSIX
    elif nombre_os == 'java':
        return 'Java'
    else:
        return 'Otro'


# Set Configs Routes and Files
CONFIG_DIR = Path.home() / '.config' / 'mt_triad'
CONFIG_FILE = CONFIG_DIR / 'mt_triad.ini'
CATEGORIES_FILE = CONFIG_DIR / 'categories.json'

# Rutas de archuivos por defecto (Desareollo)
DEV_DATA_DIR = Path(__file__).resolve().parent / 'data'
DEFAULT_CONFIG_FILE = DEV_DATA_DIR / 'default.ini'
DEFAULT_CATEGORIES_MAP = DEV_DATA_DIR / 'categories.json'

def setup_logs(settings):
    '''Configura el logging basado en el archivo de configuracion'''

    # Configurar logging
    log_level_str = settings.get("GLOBAL", "log_level", fallback="INFO").upper()

    # Mapeo de niveles paea el log
    log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR":logging.ERROR,
            "CRITICAL": logging.CRITICAL
            }
    log_level = log_levels.get(log_level_str, logging.INFO)
    logging.basicConfig(
            level=log_level,
            format="[%(levelname)s] %(message)s",
            force=True
            )

    logging.debug(f'Archivo de configuracion leido de {CONFIG_FILE}')
    
    logging.debug(f'LOG LEVEL establecido correctamente como {log_level}')


def load_default_configs():
    # Cargar archivo de cokfiguraciones por defecto
    try:
        config = ConfigParser()
        config.read(DEFAULT_CONFIG_FILE)
        return config
    except Exception as e:
        logging.error(f'Error cargando configuracion por defecto {e}')
        return ConfigParser()


def load_default_categories():
    # Carga archico de categorias por defecto
    try:
        with open(DEFAULT_CATEGORIES_MAP) as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error cargando categorías por defecto: {e}")
        return {}


def load_configs(func):
    '''Decorar nuestra funcion con carga de configuraciones dursnte ejecució'''
    def wrapper(*args, **kwargs):
        # Crear logs temporales para Debug
        logging.basicConfig(
                level=logging.DEBUG,
                format="[%(levelname)s] — %(message)s."
                )
        logging.debug('LOGS iniciales establecidos en nivel DEBUG')

        # Crear directorio de configuraciones de usuario
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        logging.debug(f'Directorio de configuracion de usuarios creado exitosamente en {CONFIG_DIR}')

        # Crear archivo de configuraciones de usuario
        if not CONFIG_FILE.exists():
            logging.debug(f'Creando archivo de configuraciones de usuario en {CONFIG_FILE}')
            default_values = load_default_configs()
            logging.debug('Valores por defecto leidos exitosamente')
            with open(CONFIG_FILE, 'w') as f:
                default_values.write(f)
            logging.debug('Configuraciones de usuario creadas')

        # Crear mapa de categorias por defecto
        if not CATEGORIES_FILE.exists():
            logging.debug(f'Creando mapa de categorias de usuario en {CATEGORIES_FILE}')
            default_values = load_default_categories()
            with open(CATEGORIES_FILE, 'w') as f:
                json.dump(default_values, f, indent=4)
            logging.debug('Mapa de categorias creado')
        
        # Cargar configuraciones de usuarios
        settings = ConfigParser()
        settings.read(CONFIG_FILE)

        # Configuramos logs globales en base a configuraciones de usuarios
        setup_logs(settings)
        
        # retorno de funcion decorada
        return func(settings,*args, **kwargs)
    return wrapper
