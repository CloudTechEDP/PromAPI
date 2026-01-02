
import os
target_dir="./"
database_path = os.path.join(target_dir, "database")
os.makedirs(database_path, exist_ok=True)
print("Database criada em:", database_path)

import sys
import shutil
import uvicorn

from modules.middleware.master import *
SHOW_DOCS = os.getenv("SHOW_DOCS", "false").lower()

with open(".env", "w") as f:
    f.write("OPENROUTER_API_KEY=SetYourKeyHere\n")
        

def extract_embedded_files():
    """
    Copia todos os arquivos incluídos no executável para target_dir.
    Funciona tanto no modo --onefile quanto no modo normal.
    """
    if getattr(sys, 'frozen', False):  # Executável PyInstaller
        base_path = sys._MEIPASS
    else:  # Modo desenvolvimento
        base_path = os.path.abspath(".")

    # Listar todos os diretórios que queremos copiar
    dirs_to_copy = ["templates", "static", "modules"]

    for d in dirs_to_copy:
        src = os.path.join(base_path, d)
        dst = os.path.join(target_dir, d)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)  # Remove antiga, se existir
            shutil.copytree(src, dst)
    return target_dir

# Uso no início do programa
extract_embedded_files()





app = FastAPI(
    docs_url=None if SHOW_DOCS != "true" else "/docs",
    redoc_url=None if SHOW_DOCS != "true" else "/redoc",
    openapi_url=None if SHOW_DOCS != "true" else "/openapi.json",
)

app.include_router(index_router)
app.include_router(gauge_router)
app.include_router(counter_router)
app.include_router(aggregate_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import webbrowser

    webbrowser.open("http://localhost:8000")

    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

    server = uvicorn.Server(config)
    server.run()
