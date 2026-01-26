


from util.logging import logging
import sys
from util.ErrorMessages import error_message_box
from util.ExtractFiles import extract_embedded_files
from util.winService import win_service_setup, win_service_start, service_exists_and_path
from util.LinuxService import linux_service_setup
from util.DetectPlataform import plataform_detect
args = sys.argv[1:]
logging.info("Argumentos recebidos: %s", args)

def startup():
    logging.info("Starting PromAPI application...")
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
    server = uvicorn.Server(config)
    server.run()

sistema = plataform_detect()
def install():
    logging.info("Iniciando extração de arquivos incorporados...")
    extract_embedded_files()
    logging.info("Arquivos extraídos com sucesso.")
    if sistema == "Windows":
        logging.info("Iniciando instalação...")
        win_service_setup()
        win_service_start()
        logging.info("Windows service setup complete.")
    elif sistema == "Linux":
        logging.info("Iniciando instalação...")
        linux_service_setup()
        logging.info("Linux service setup complete.")
    else:
        logging.info("Outro sistema: %s", sistema)
    logging.info("Sistema: %s", sistema)

if args == ["start"]:
    if not os.path.exists("static") or not os.path.exists("templates") or not os.path.exists("modules"):
        extract_embedded_files()
    logging.info("Iniciando APP...")
    from main import *
    startup()
elif args == ["install"]:
    install()
else:
    logging.info("Nenhum argumento de serviço fornecido.")
    if sistema == "Windows":
        error_message_box(
            "Ops, esse instalador deve ser usado via CLI (Administrador):\n " \
            "PromAPI.exe install  - para instalar o serviço\n " \
            "PromAPI.exe start    - para iniciar o serviço sem instalá-lo"
            )





