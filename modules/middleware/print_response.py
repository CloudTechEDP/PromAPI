
from modules.middleware.master import *

def print_response(response):
    # Obtém o quadro do chamador
    quadro_chamador = inspect.stack()[1]
    nome_funcao_chamadora = quadro_chamador.function
    print(f"\033[32mFUNÇÃO CHAMADORA: {nome_funcao_chamadora}\033[0m")

    print(response, flush=True)
    print("+=+"*20, flush=True)
    return response