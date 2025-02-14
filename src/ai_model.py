import ollama

def extract_invoice_data(text) -> str:
    prompt = (
        "Extraia os seguintes valores do texto abaixo: Beneficiário ou Cedente, CPF/CNPJ do Beneficiário ou Cedente, "
        "Sacado ou Pagador, CPF/CNPJ do Sacado ou Pagador, Vencimento e Valor do Documento.\n\n"

        " Regras importantes:\n"
        "- O Beneficiário ou Cedente deve ser extraído separadamente do seu CPF/CNPJ. Não os combine.\n"
        "- O Beneficiário ou Cedente aparece sempre próximo ao nome 'Beneficiário' ou 'Cedente'.\n"
        "- Não confunda nomes genéricos como 'Caixa', 'Pagador', 'Beneficiário', 'Avalista' ou 'Banco' com o Beneficiário correto.\n"
        "- O CPF/CNPJ do Beneficiário ou Cedente deve estar no formato correto (ex: 00.000.000/0000-00, 00.000.000/0000.00 ou 000.000.000-00).\n"
        "- O CPF/CNPJ do Sacado também deve estar no formato correto.\n"
        "- O Vencimento deve ser extraído logo após o termo 'Vencimento' e está no formato dd/mm/yyyy\n"
        "- O 'Valor do Documento' pegue o numero depois do termo 'Valor do Documento', não extraia valores encontrados antes.\n"
        "- Se não houver um valor claramente identificado em algum listado, coloque 'None' no valor dele.\n\n"

        f" Texto do documento:\n{text}\n\n"

        "Responda sem formatação de texto apenas com os valores igual o exemplo abaixo:\n"
        "Beneficiário ou Cedente: <somente o nome da empresa ou pessoa>\n"
        "CPF/CNPJ do Beneficiário ou Cedente: <somente o CPF/CNPJ>\n"
        "Sacado: <somente o nome da empresa ou pessoa>\n"
        "CPF/CNPJ Sacado: <somente o CPF/CNPJ>\n"
        "Vencimento: <data>\n"
        "Valor do Documento: R$ <valor>\n"
    )
    
    response = ollama.chat(model='llama3.1:8b-instruct-q4_K_M', messages=[{"role": "user", "content": prompt}], options={"temperature": 0.0})    
    return response['message']['content']