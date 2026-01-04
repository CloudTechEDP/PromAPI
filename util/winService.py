def service_exists_and_path(service_name, exe_path):
    import win32serviceutil
    import win32service
    import pywintypes
    try:
        # Verifica se o serviço existe
        status = win32serviceutil.QueryServiceStatus(service_name)
    except Exception:
        return False, None
    try:
        # Abre o gerenciador de controle de serviço
        hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        hsrv = win32service.OpenService(hscm, service_name, win32service.SERVICE_QUERY_CONFIG)
        config = win32service.QueryServiceConfig(hsrv)
        win32service.CloseServiceHandle(hsrv)
        win32service.CloseServiceHandle(hscm)
        # config[3] é o caminho do executável
        exe_on_service = config[3].strip('"')
        return True, exe_on_service == exe_path
    except pywintypes.error:
        return True, None


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.ErrorMessages import error_message_box



def win_service_setup():
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    import sys
    import os

    import traceback
    import os
    SERVICE_NAME = "PromAPI"
    SERVICE_DISPLAY_NAME = "PromAPI"

    # Caminho absoluto do executável
    import traceback
    exe_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    script_path = os.path.join(exe_dir, "PromAPI.exe")

    if not os.path.exists(script_path):
        error_message_box(f"PromAPI.exe não encontrado em: {script_path}")
        return
    
    exists, path_ok = service_exists_and_path(SERVICE_NAME, script_path)
    if exists:
        if path_ok:
            error_message_box(f"O serviço {SERVICE_NAME} já existe e aponta para o executável correto. Não será reinstalado.")
            return
        else:
            error_message_box(f"O serviço {SERVICE_NAME} já existe, mas aponta para outro executável. Remova ou ajuste manualmente.")
            return
    else:
        try:
            win32serviceutil.InstallService(
                pythonClassString=None,
                serviceName=SERVICE_NAME,
                displayName=SERVICE_DISPLAY_NAME,
                startType=win32service.SERVICE_AUTO_START,
                exeName=script_path,
                exeArgs='start',
                description="Prometheus API Service"
            )
            error_message_box(f"Serviço {SERVICE_NAME} instalado com sucesso.")
        except Exception as e:
            tb = traceback.format_exc()
            error_message_box(f"Erro ao instalar o serviço: {e}\n{tb}")
            return

def win_service_start():
    import win32serviceutil
    SERVICE_NAME = "PromAPI"
    try:
        win32serviceutil.StartService(SERVICE_NAME)
    except Exception as e:
        error_message_box(f"Erro ao iniciar o serviço {SERVICE_NAME}: {e}")