from modules.middleware.master import *
import logging
import requests
logging.info(" middleware Logs initialized.")

def logging_app():
    """
    Initialize application logging.
    
    Creates a "logs" directory adjacent to the executed script, builds a dated log filename that includes the log level, and configures Python logging to write to that file and to the console.
    """
    try:
        print("Initializing logging middleware...")
        LOG_LEVEL = "Debug"
        hoje = datetime.now()
        dia = hoje.day
        mes = hoje.month
        # Garante que o diretório logs será criado na raiz do projeto
        # root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        root_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        log_dir = os.path.join(root_dir, "logs")
        print(f"[LOGGING] Diretório de logs será: {log_dir}")
        os.makedirs(log_dir, exist_ok=True)
        filename = f"{hoje.year}-{mes:02d}-{dia:02d}-{LOG_LEVEL.upper()}"
        log_file = os.path.join(log_dir, filename + ".log")
        print(f"[LOGGING] Arquivo de log será: {log_file}")
        logging.basicConfig(
            level=logging.getLevelName(LOG_LEVEL.upper()),
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ],
            force=True  
        )
        print(f"Logging initialized. Log file: {log_file}")
    except Exception as e:
        print(f"Error initializing logging middleware: {e}")

# async def log_status_code_middleware(request: request, call_next):
#     response = await call_next(request)
#     ip = request.headers.get("x-forwarded-for", request.client.host)
#     status_code = response.status_code
#     path = request.url.path
#     logging.info(f"{ip} {path} {status_code}")
#     return response

logging_app()