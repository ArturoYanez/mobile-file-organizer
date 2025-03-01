import os
import platform

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
        os.makedirs('/data/data/com.termux/files/home/.config/mt_triad/')
        print('Fichero creado correctamente')
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

# Ejemplo de uso
sistema_operativo = obtener_sistema_operativo()
print(f"El sistema operativo es: {sistema_operativo}")
