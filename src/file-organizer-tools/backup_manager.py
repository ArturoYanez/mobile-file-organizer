import os
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED


def create_backup(source_dir: str):
    timestamp = datetime.now().strftime("%d%m%y_%H%M%S")
    zip_name = f'backup_{timestamp}.zip'
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

create_backup(os.getcwd())
