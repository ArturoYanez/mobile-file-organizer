import logging
import argparse
import logging
from pathlib import Path
import config
import file_organizer as fo
import backup_manager as bm


@config.load_configs
def main(settings):
   
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

        # Recibir ruta de argunento y convertir a objeto Path
        directory_path = Path(Path.home() / args.o)

        # Recibir lista de ezclusiones de configuraciones
        exclude_list = settings.get('FILE_ORGANIZER', 'exclude_patter').split(' ')

        # Validar si el ddirectorio existe
        if not directory_path.exists():
            logging.error(f"Directorio no encontrado: {directory_path}")
            return

        # Pasar parametros a modulo organizsr archivos
        fo.organizer(
                directory_path,
                config.CATEGORIES_FILE,
                exclude_list)

    elif args.b:
        # Recibir input y conbertir a instancis de Path
        directory_path = Path(Path.home() / args.b)

        # Obtener ruta de output de configuraciones
        output_path = Path(settings.get("BACKUP_CREATOR", "output_path", fallback='mt_triad/backup'))
        if not directory_path.exists():
            logging.error(f"Directorio no encontrado: {directory_path}")
            return
        bm.create_backup(directory_path,output_path)

if __name__ == '__main__':
    main() 
