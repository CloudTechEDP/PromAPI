
from modules.middleware.master import *

def print_response(response):
    # Obtém o quadro do chamador
    quadro_chamador = inspect.stack()[1]
    nome_funcao_chamadora = quadro_chamador.function
    print(f"\033[32mFUNÇÃO CHAMADORA: {nome_funcao_chamadora}\033[0m")

    print(response, flush=True)
    print("+=+"*20, flush=True)
    return response


def try_catch_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"\033[31mERRO na função {func.__name__}: {str(e)}\033[0m", flush=True)
            raise e
    return wrapper