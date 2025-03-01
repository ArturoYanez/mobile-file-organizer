import os
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED


def create_backup(source_dir):
    backup_dir = os.path.join(source_dir,'backups')
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
    zip_name = os.path.join(backup_dir,f'backup_{timestamp}.zip')
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            if backup_dir in root:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    print(f'file {zip_name} created successfully')
