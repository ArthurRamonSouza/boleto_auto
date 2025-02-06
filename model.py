import ollama
import time

text = """"sem proc

Obs: Pagar Preferencialmente nas Casas Lotéricas

CAIXA:::104-0

RECIBO DO SACADO

[Cedente

FAgêncialCódigo Cedente

Conselho Regional de Enfermagem - Sergipe

2382/070212-9

Vencimento 31/03/2015

[Data do Documento

[Nº do Documento

Espécie Doc

JAceite

[Data do Processamento

08/11/2012

|Nosso Número

24000000001108643-6

F da ConlalRespo.

[Carteira

SR

Espécie

R$

[Quantidade

| Valor
x
L

|] Valor do Documento
R$ 315,28

Instruções:
Anuidade: 2016.
COTA ÚNICA = R$ 315,28

**AO BANCO: APÓS VENC.COBRAR MULTA 2% + JUROS 1% A.M**

[-) Desconto

|') Outras Deduções/Abatimento

[5] MoraMultarJuros

|) Outros Acrescimos

|”) Valor Cobrado

Emitido por: Guilherme Diangelis Gomes

[Sacado
GUILHERME DIANGELIS GOMES
Conj Maria do Carmo
49092-540 Aracaju

Nº da Inscrição:
OLARIA cPFiCGC: 000.000.000-00

SE

O documento de agendamento de pagamento
iti ixa rapido não e valido

lo pelo

CAIXA=::104-0

10490.70210 29000.200047 00110.864303 6 55330000031528

[TT utenticação Mecânica

[Local de Pagamento

PAGÁVEL NA REDE BANCÁRIA ATÉ O VENCIMENTO

Vencimento 31/03/2015

[Codente

Agência/Código Cedente

Conselho Regional de Enfermagem - Sergipe

2382/070212-9

[Data do Documento [Nº do Documento Espécie Doc

JAceite

[Data do Processamento

08/11/2012

[Nosso Númer

24000000001 108643-6

F da ConlalRespo. [Carteira Espécie

R$

[Quantidade

| Valor
x
L

|] Valor do Documento
R$ 315,28

Instruções:
Anuidade: 2016.
COTA ÚNICA = R$ 315,28

Emitido por: Guilherme Diangelis Gomes

**AO BANCO: APÓS VENC.COBRAR MULTA 2% + JUROS 1% A.M**

[-) Desconto

|') Outras Deduções/Abatimento

[5] MoraMultarJuros

+) Outros Acrescimos

|”) Valor Cobrado

|sacado.

Conj Maria do Carmo

E

OLARIA

Nº da Inscrição:

CPFICGC: 000.000.000-0

GUILHERME DIANGELIS GOMES

49092-540 Aracaju

s

[TT tentcação Mecânica

Esse documento deverá ser guardado por no

FICHA DE COMPENSAÇÃO

mínimo 5 anos

"""

def extract_invoice_data(text):
    start_time = time.time() 

    prompt = (
        "Extraia os valores de: Cedente, Código do Cedente, Sacado, CPF/CNPJ, "
        "Vencimento, Valor do Documento, Nosso Número, Data do Processamento, do texto:\n"
        f"{text}\n\n"
        "A resposta deve ser somente os dados encontrados, não adicione nada na sua resposta e use o seguinte formato:\n"
        "Cedente: <valor>\n"
        "Código do Cedente: <valor>\n"
        "Sacado: <valor>\n"
        "CPF/CNPJ: <valor>\n"
        "Vencimento: <valor>\n"
        "Valor do Documento: <valor>\n"
        "Nosso Número: <valor>\n"
        "Data do Processamento: <valor>"
    )
    
    response = ollama.chat(model='llama3.1:8b-instruct-q4_K_M', messages=[{"role": "user", "content": prompt}])
    # response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])
    # response = ollama.chat(model='llama3:8B', messages=[{"role": "user", "content": prompt}])


    end_time = time.time()
    
    elapsed_time = end_time - start_time  # Calcula o tempo decorrido
    print(f"Tempo de processamento: {elapsed_time:.2f} segundos")
    
    return response['message']['content']

# Exemplo de uso
resultado = extract_invoice_data(text)
print(resultado)