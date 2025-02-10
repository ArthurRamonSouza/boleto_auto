# 📖 Descrição do Projeto
Este projeto processa faturas em PDF enviadas por e-mail, extrai dados como códigos de barras e imagens, e salva as informações em um banco de dados. Utiliza bibliotecas de OCR, análise de imagem e LLM para automatizar o processamento e estruturação das faturas.

# 🚀 Como Instalar e Rodar
## Requisitos
Para rodar o executável corretamente, sua máquina precisa das seguintes dependências instaladas:
- **Python 3.12**
- **Tesseract OCR**
- **MySQL**
- **Ollama e modelo llama3.1:8b-instruct-q4_K_M**
- **Bibliotecas Python** (instaladas automaticamente ao rodar o executável)

### Rodando o Executável
Se estiver usando a versão compilada:
```sh
./boleto_auto
```
Ou no Windows:
```sh
boleto_auto.exe
```

# ⚙️ Tecnologias Usadas
- **Python 3.12**
- **OpenCV** (processamento de imagem)
- **Tesseract OCR** (reconhecimento de texto)
- **Pyzbar** (leitura de códigos de barras)
- **SQLAlchemy** (interação com o banco de dados)
- **pdf2image** (conversão de PDF em imagens)
- **Ollama** (carregar modelo LLM para processamento dos textos)

# 📜 Explicação dos Módulos Principais

### `main.py`
- Gerencia o fluxo principal da aplicação, chamando os módulos de leitura, extração e armazenamento de faturas.

### `invoice_reader.py`
- Lê e processa faturas em PDF, convertendo-as em imagens e extraindo informações relevantes.

### `model.py`
- Responsável por enviar o texto extraído das faturas para um modelo LLaMA, que processa e retorna informações estruturadas.

### `database.py`
- Gerencia a conexão com o banco de dados e a persistência das informações extraídas.

Essa documentação fornece um guia rápido para instalação, uso e entendimento dos principais componentes do projeto. Caso precise de mais detalhes, basta avisar! 🚀

