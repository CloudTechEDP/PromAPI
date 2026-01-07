import os
import win32serviceutil
import sys
from util.ErrorMessages import error_message_box
SERVICE_NAME = "PromAPI"
SERVICE_DISPLAY_NAME = "PromAPI"
ROOT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
UTIL_DIR = os.path.join(ROOT_DIR, "util")

def service_exists_and_path():
    """
    Check whether the Windows service identified by SERVICE_NAME is present and queryable.
    
    Returns:
        bool: `True` if the service exists and its status could be queried, `False` otherwise.
    """
    try:
        status = win32serviceutil.QueryServiceStatus(SERVICE_NAME)
        return True
    except Exception:
        return False

def win_service_setup():
    """
    Create a WinSW XML configuration for the PromAPI service, write it to the utilities directory, and invoke the WinSW installer to install the service.
    
    Writes a file named "WinSW.xml" under UTIL_DIR containing the service definition (service id, name, description, executable path, arguments, working directory, log mode, and failure action), then runs the WinSW.exe install command in UTIL_DIR which attempts to install the Windows service. This function performs filesystem writes and executes an external system command.
    """
    createfile = f"""
    <service>
        <id>{SERVICE_NAME}</id>
        <name>{SERVICE_NAME}</name>
        <description>{SERVICE_NAME} Service</description>

        <executable>{ROOT_DIR}\PromAPI.exe</executable>
        <arguments>start</arguments>
        <workingdirectory>{ROOT_DIR}</workingdirectory>

        <logmode>rotate</logmode>

        <onfailure action="restart" delay="15 sec"/>
    </service>
    """
    service_file_path = os.path.join(UTIL_DIR, "WinSW.xml")
    with open(service_file_path, "w") as f:
        f.write(createfile)
    comandline = f'{UTIL_DIR}\\WinSW.exe install'
    os.system(comandline) # Executa o comando para instalar o serviço

def win_service_start():
    """
    Start the PromAPI Windows service and display a success message box with the local access URL.
    
    This function invokes the WinSW start command from the utilities directory to start the service, then shows a message informing the user that the service has been started and where to access the application.
    """
    comandline = f'{UTIL_DIR}\\WinSW.exe start'
    os.system(comandline) # Executa o comando para iniciar o serviço
    error_message_box("Serviço PromAPI iniciado com sucesso!\n" \
    "aguarde alguns segundos enquanto a aplicação é carregada.\n" \
    "\n" \
    "Você pode acessar a aplicação em: http://localhost:8000 logo apos fechar essa janela")