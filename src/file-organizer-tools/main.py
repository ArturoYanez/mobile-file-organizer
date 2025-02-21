import file_organizer as fo
import backup_manager as bm
import password_validator as pv
import argparse
from art import *

def main():
    parser = argparse.ArgumentParser(description='Paquete de herramientas para gestion de archicos empresarialws. Organizsr archivos de directorios concreros por extension, validar seguridad de contraseñas en ficheros CSV por criterios, y crear copias de seguridad en archivos ZIP locales.')
    parser.add_argument('-o', metavar='RUTA_DIRECTORIO', help='Organizar archivos')
    parser.add_argument('-p', metavar='RUTA_ARCHIVO', help='Validar contraseñas de archivo CSV')
    parser.add_argument('-b',metavar='RUTA_DIRECTORIO', help='Realizar Backup de ficheros en ZIP')


    args = parser.parse_args()
    
    tprint(' MT\nTriad ', font='roman')
    print(f'\tCreated by: ArturoYanez\n')
    if args.o:
        directory_path = args.o
        fo.organizer(directory_path)
    elif args.b:
        directory_path = args.b
        bm.create_backup(directory_path)
    elif args.p:
        file_path = args.p
        pv.get_data(file_path)

if __name__ == '__main__':
    main()
