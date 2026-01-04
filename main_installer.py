


from util.logging import *
import sys
from util.ErrorMessages import error_message_box
from util.ExtractFiles import extract_embedded_files
from util.winService import *
from util.LinuxService import *
from util.DetectPlataform import plataform_detect
import webbrowser

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
    
    if sistema == "Windows":
        win_service_setup()
        win_service_start()
        logging.info("Windows service setup complete.")
    elif sistema == "Linux":
        linux_service_setup()
        logging.info("Linux service setup complete.")
    else:
        logging.info("Outro sistema:", sistema)

    logging.info("Sistema detectado:", sistema)


args = sys.argv[1:]
logging.info("Argumentos recebidos: %s", args)

if args == ["start"]:
    extract_embedded_files()
    from main import *
    startup()
elif args == ["install"]:
    extract_embedded_files()
    from main import *
    install()
else:
    logging.info("Nenhum argumento de serviço fornecido.")
    if sistema == "Windows":
        error_message_box(
            "Ops, esse instalador deve ser usado via CLI (Administrador):\n " \
            "PromAPI.exe install  - para instalar o serviço\n " \
            "PromAPI.exe start    - para iniciar o serviço sem instalá-lo"
            )






# def is_service_mode():
#     return '--service' in sys.argv

# if __name__ == "__main__":
#     if sistema == "Windows":
#         win_service_setup(service_args='--service')
#     elif sistema == "Linux":
#         linux_service_setup()
#         print("Linux service setup complete.")
#     else:
#         print("Outro sistema:", sistema)

#     if not is_service_mode():
#         # Manual start: open browser and run app
#         from main import *
#         webbrowser.open("http://localhost:8000")
#         config = uvicorn.Config(
#             app=app,
#             host="0.0.0.0",
#             port=8000,
#             reload=False,
#             log_level="info"
#         )
#         server = uvicorn.Server(config)
#         server.run()
#     else:
#         # Service mode: just run app, no browser
#         from main import *
#         config = uvicorn.Config(
#             app=app,
#             host="0.0.0.0",
#             port=8000,
#             reload=False,
#             log_level="info"
#         )
#         server = uvicorn.Server(config)
#         server.run()


