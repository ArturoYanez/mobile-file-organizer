from pathlib import Path
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
import logging


def create_backup(source_dir: Path, output_path: Path):

    # Crear directorio de backups
    backup_dir = Path.home() / output_path
    
    # Crear el directorio si no existe
    if not backup_dir.exists():
        backup_dir.mkdir(parents=True)
    
    # Establecer fecha y hora de creacion de copia de seguridad
    timestamp = datetime.now().strftime("%d%m%y_%H%M%S")

    # Creae nombre de archivo para copia de seguridad
    zip_name = backup_dir / f'backup_{timestamp}.zip'

    # Crear copia de seguridad
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zipf:

        # Recorree archivos en el directorio solicitado
        for file_path in source_dir.rglob('*'):

            # Ignorar directorio paea backups
            if backup_dir in file_path.parents or file_path == backup_dir:
                continue

            # Guardar ruta relariva de archivo en relacion a la ruta objetivo
            arcname = file_path.relative_to(source_dir)

            # Comprimir nuestro archivo en el backup
            zipf.write(file_path, arcname)
    logging.info(f'file {zip_name} created successfully')
