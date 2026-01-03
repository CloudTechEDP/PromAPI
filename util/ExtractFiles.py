
import stat


def extract_embedded_files():
    from util.ErrorMessages import error_message_box
    import shutil
    import sys
    import os
    permission = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO  # 777
    try:
        target_dir="./"
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        dirs_to_copy = ["templates", "static", "modules"]

        for d in dirs_to_copy:
            src = os.path.join(base_path, d)
            dst = os.path.join(target_dir, d)
            if os.path.exists(src):
                # if os.path.exists(dst):
                #     shutil.rmtree(dst)
                shutil.copytree(src, dst, dirs_exist_ok=True)
                os.chmod(os.path.join(dst), permission)
                for file in os.listdir(dst):
                    os.chmod(os.path.join(dst, file), permission)
  
        os.chmod(target_dir, permission)
    except Exception as e:
        error_message_box(
            f"Ocorreu um erro ao tentar extrair os arquivos necessários para o funcionamento do programa:\n\n{e}\n\n"
            f"Você precisa ser administrador local com permissões de escrita no diretório onde o programa está sendo executado.\n\n"
            f"Tipo do erro: {sys.exc_info()[0]}"
        )
    return target_dir

