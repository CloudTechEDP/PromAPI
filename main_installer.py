

import sys
from util.ErrorMessages import error_message_box
from util.ExtractFiles import extract_embedded_files
from util.winService import *
from util.LinuxService import *
from util.DetectPlataform import plataform_detect
import webbrowser

extract_embedded_files()
sistema = plataform_detect()
print("Sistema detectado:", sistema)

with open(".env", "w") as f:
    f.write("OPENROUTER_API_KEY=SetYourKeyHere\n")

def is_service_mode():
    return '--service' in sys.argv

if __name__ == "__main__":
    if sistema == "Windows":
        win_service_setup(service_args='--service')
    elif sistema == "Linux":
        linux_service_setup()
        print("Linux service setup complete.")
    else:
        print("Outro sistema:", sistema)

    if not is_service_mode():
        # Manual start: open browser and run app
        from main import *
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
    else:
        # Service mode: just run app, no browser
        from main import *
        config = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
        server = uvicorn.Server(config)
        server.run()


