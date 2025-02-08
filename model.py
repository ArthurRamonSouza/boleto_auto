import ollama
# import time

def extract_invoice_data(text) -> str:
    # start_time = time.time() 

    prompt = (
        "Extraia os seguintes valores do texto abaixo: Beneficiário ou Cedente, CPF/CNPJ do Beneficiário ou Cedente, "
        "Sacado ou Pagador, CPF/CNPJ do Sacado ou Pagador, Vencimento, Valor do Documento, "
        "e Data do Processamento ou Data de Emissão.\n\n"
        
        " Regras importantes:\n"
        "- O Beneficiário ou Cedente deve ser extraído separadamente do seu CPF/CNPJ. Não os combine.\n"
        "- O Beneficiário ou Cedente geralmente aparece próximo ao 'Agência/Código Cedente'.\n"
        "- Não confunda nomes genéricos como 'Caixa' ou 'Banco' com o Beneficiário correto.\n"
        "- O CPF/CNPJ do Beneficiário ou Cedente deve estar no formato correto (ex: 00.000.000/0000-00 ou 000.000.000-00).\n"
        "- O CPF/CNPJ do Sacado também deve estar no formato correto.\n"
        "- O Vencimento deve ser extraído exatamente como aparece no documento e o formato é dd/mm/yyyy.\n"
        "- O Valor do Documento está localizado perto de 'Valor do Documento' e é o malor valor em reais.\n"
        "- Se algum valor não for encontrado no texto, retorne o valor como 'None'.\n\n"

        f" Texto do documento:\n{text}\n\n"

        "Responda sem formatação de texto apenas com os valores igual o exemplo abaixo:\n"
        "Beneficiário ou Cedente: <somente o nome da empresa ou pessoa>\n"
        "CPF/CNPJ do Beneficiário ou Cedente: <somente o CPF/CNPJ>\n"
        "Sacado: <somente o nome da empresa ou pessoa>\n"
        "CPF/CNPJ Sacado: <somente o CPF/CNPJ>\n"
        "Vencimento: <valor>\n"
        "Valor do Documento: R$ <valor>\n"
    )

    
    response = ollama.chat(model='llama3.1:8b-instruct-q4_K_M', messages=[{"role": "user", "content": prompt}])
    # response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])
    # response = ollama.chat(model='llama3:8B', messages=[{"role": "user", "content": prompt}])

    # end_time = time.time()
    
    # elapsed_time = end_time - start_time  # Calcula o tempo decorrido
    # print(f"Tempo de processamento: {elapsed_time:.2f} segundos")
    
    return response['message']['content']