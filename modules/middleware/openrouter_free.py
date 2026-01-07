from modules.middleware.master import *

API_TOKEN = os.getenv("OPENROUTER_API_KEY", "false_key")


def ask_gepeto(error, raw_body):
    """
    Generate an AI-proposed, concise solution in Portuguese for a reported error and its POST payload.
    
    Parameters:
        error: The original error message or exception to be analyzed.
        raw_body: The raw POST payload (string or dict) associated with the error.
    
    Returns:
        ia_solution (str): A Portuguese (ptbr) solution text (≈100 words) with one example of a correct metric submission.
    
    Notes:
        If the OpenRouter API key is not configured, a warning message is emitted and no AI call is made. The function records the error and AI solution via log_error and prints the resulting database log ID.
    """
    from openai import OpenAI
    if API_TOKEN == "false_key":
        return print_response("⚠️ OPENROUTER_API_KEY não está definido. O middleware OpenRouter Free não será carregado.")
    if API_TOKEN.startswith("sk-or-"):
        print_response("✅ OPENROUTER_API_KEY detectado. Middleware OpenRouter Free carregado com sucesso.")

    client = OpenAI(
        api_key=API_TOKEN,
        base_url="https://openrouter.ai/api/v1"
    )
    print_response("Consultando IA para solução do erro...")
    response = client.chat.completions.create(
        model="allenai/olmo-3.1-32b-think:free",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Analise o API POST {raw_body} o erro {error} e proponha uma solução:\n"
                    f" verifique se os dados inseridos não estão no padrão aceito pelo Prometheus. "
                    f" verifique erros do python. "
                    f" sugira correções objetivas e práticas. "
                    f"Responda em no máximo 100 palavras. "
                    f"Responda apenas com a solução, sem saudações ou introduções. "
                    f"de 1 exemplo de como enviar a métrica corretamente. "
                    f"Resposta em português ptbr. "
              
                )
            }
        ]
    )
    ia_solution = response.choices[0].message.content
    errorlog = log_error(error, raw_body, ia_solution)
    print_response(f"Erro registrado no banco de dados com ID: {errorlog['id']}")
    return ia_solution