import os
import shutil
categories = {
        'documents': {
            'text': ('.txt', '.md', '.rtf'),
            'microsoft': ('.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'),
            'open': ('.odt', '.odp', '.ods'),
            'pdf': ('.pdf'),
            'latex': ('.tex',)
            },
        'images': {
            'rasterize': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'),
            'vector': ('.svg', '.eps', '.ai'),
            'photoshop': ('.psd',),
            'coreld': ('.cdr',)
            },
        'videos': ('.mp4', '.avi', '.mov', '.wmv', '.fiv', '.mkv'),
        'audios': ('.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma'),
        'compress': ('.zip', '.rar', '.tar', '.gz', '.7z'),
        'code': {
            'source': {
                'python': ('.py',),
                'javascript': ('.js',),
                'html': ('.html',),
                'css': ('.css',),
                'java': ('.java',),
                'c++': ('.cpp',),
                'c#': ('.cs',)
                },
            'scripts': ('.sh', '.bat', '.ps1')
            },
        'databases': ('.sql', '.db', '.mdb', '.accbd'),
        'logs': ('.log',),
        'other': ('.ini', '.cfg', '.conf')
        }

def check_ext(file_extension, extension_map, category_path = None):
    if category_path is None:
        category_path = []
    for key, value in extension_map.items():
        if isinstance(value, tuple):
            if file_extension in value:
                return True, category_path + [key]
        elif isinstance(value, dict):
            found, path = check_ext(file_extension, value, category_path + [key])
            if found:
                return found, path 
    return False, []


def organizer(directory: str):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        print(f'path: {path}')
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            print(f' ext: {ext}')
            found, c_path = check_ext(ext, categories)
            if found:
                n_directory = directory
                for paths in c_path:
                    n_directory = os.path.join(n_directory, paths)
                if not os.path.exists(n_directory):
                    os.makedirs(n_directory)
                    print('direcoty created')
                shutil.move(path,n_directory)
            else:
                print(f'Category dont exits')
    print('Operation success!!!')

cwd = os.getcwd()

