import os
import stat
root_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
permission = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO 
removedirs = ['build', 'dist']
for rmdir in removedirs:
    dir_path = os.path.join(root_dir, rmdir)
    os.chmod(dir_path, permission)
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f'Removing directory: {dir_path}')
        import shutil
        def on_rm_error(func, path, exc_info):
            # Remove read-only and try again
            os.chmod(path, stat.S_IWRITE)
            func(path)

        shutil.rmtree(dir_path, onerror=on_rm_error)

os.system(f'pyinstaller --name PromAPI --onefile --add-data "util;util" --add-data "templates;templates" --add-data "static;static" --add-data "modules;modules" {root_dir}/main_installer.py')
