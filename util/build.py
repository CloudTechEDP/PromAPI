import os
import stat
root_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
# permission = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO 
# set permissions to 755
permission = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
             stat.S_IRGRP | stat.S_IXGRP | \
                stat.S_IROTH | stat.S_IXOTH

removedirs = ['build', 'dist']
try:
    import shutil
    shutil.rmtree(os.path.join(root_dir, '__pycache__'))
    for rmdir in removedirs:
        dir_path = os.path.join(root_dir, rmdir)
        os.chmod(dir_path, permission)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f'Removing directory: {dir_path}')
            def on_rm_error(func, path, exc_info):
                # Remove read-only and try again
                os.chmod(path, stat.S_IWRITE)
                func(path)

            shutil.rmtree(dir_path, onerror=on_rm_error)
except Exception as e:
    print(f'Error removing directories: {e}')
try:
    os.system(f'pyinstaller --name PromAPI --onefile --add-data "util;util" --add-data "templates;templates" --add-data "static;static" --add-data "modules;modules" {root_dir}/main_installer.py')
except Exception as e:
    print(f'Error during build: {e}')