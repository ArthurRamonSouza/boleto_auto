import re
import cv2
import pytesseract
import numpy as np
from PIL import Image
from invoice import Invoice
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
class InvoiceReader:

    def __init__(self):
        pass

    # Pega toda a imagem de um boleto no pdf, o codigo de barras e o tipo
    def get_image_of_invoices_from_pdf(self, pdf_path: str = '', ppi: int = 300) -> list[Invoice]:
        try:
            pdf_images: list[Image.Image] = convert_from_path(pdf_path, ppi)
            invoice_list: list[Invoice] = []

            # Para cada imagem no pdf
            for image in pdf_images:
                    decoded_images: list = decode(image)

                    if not decoded_images:
                        print(f"There wasn't barcodes in this pdf page")

                    else:
                        # Captura a imagem com os dados boleto, o codigo de barras e o tipo
                        for barcode in decoded_images:
                            if barcode.data != '' and barcode.type == 'I25':
                                invoice: Invoice = Invoice(barcode.data.decode('utf-8'), 'I25')
                                invoice.image = image.copy()
                                invoice_list.append(invoice)
            return invoice_list
            
        except Exception as e:
            print(f'Error while decoding the pdf: {e}')
            return None

    # Faz a busca por texto nas imagens do boleto
    def get_data_from_invoice_image(self, invoice: Invoice) -> None:
        text = pytesseract.image_to_string(invoice.image, lang='por', config='--psm 12')
        # print(text)
        # print("============================================================================================================================================")

        invoice_data = {}

        regex_dict = {
            'bank': r'(\bBradesco\b|\bItaú\b|\bCaixa\b|\bSantander\b|\bBanco do Brasil\b)',
            # 'barcode': r'(\d{5}\.\d{5} \d{5}\.\d{6} \d \d{14})',
            'beneficiary_name': r'Beneficiário\s+(.*?)\s+-\s+CNPJ',
            'beneficiary_number': r'CNPJ\s+([\d\.\-\/]+)',
            'guantor_name': r'Sacador/Avalista\s+(.*?)\s+-\s+\d{2,3}\.\d{3}\.\d{3}\/\d{4}-\d{2}',
            'guantor_number': r'Sacador/Avalista\s+.*\s+-\s+([\d\.\-\/]+)',
            'guantor_number': r'Sacador/Avalista\s+.*\s+-\s+([\d\.\-\/]+)',
            'payer_name': r'Pagador\s+(.*?)\s+-\s+\d{3}\.\d{3}\.\d{3}-\d{2}',
            'payer_number': r'Pagador.*?(\d{3}\.\d{3}\.\d{3}-\d{2})',
            'due_date': r'Data de Vencimento\s+(\d{2}/\d{2}/\d{4})',
            'amount': r'R\$\s*([\d,]+)',
            # 'yielding_code': r'Agência / Código do Cedente\s+([\d\/\-]+)',
            'invoice_number': r'Nosso Número\s*.(\d{2}\/\d{11}-\d{1})'
        }

        # regex_dict = {
        #     'bank': r'CAIXA\s*:::\s*(\d{3}-\d)',  # Captura o código do banco (104-0 para Caixa)
        #     # 'barcode': r'(\d{5}\.\d{5} \d{5}\.\d{6} \d \d{14})',  # Captura código de barras
        #     'beneficiary_name': r'Cedente\s+([\w\s\-\./]+)',  # Nome do beneficiário
        #     'beneficiary_number': r'Agência/Código Cedente\s+([\d\/\-]+)',  # Código do Cedente
        #     'payer_name': r'Sacado\s+([\w\s]+)\s*CPF\/CNPJ:',  # Nome do pagador
        #     'payer_number': r'CPF\/CNPJ:\s*(\d{3}\.\d{3}\.\d{3}-\d{2})',  # CPF ou CNPJ do pagador
        #     'due_date': r'Vencimento\s+(\d{2}/\d{2}/\d{4})',  # Data de vencimento
        #     'amount': r'Valor do Documento\s*R\$\s*([\d,.]+)',  # Valor do boleto
        #     'invoice_number': r'Nosso Número\s+(\d{8,17}-\d)',  # Nosso Número
        #     'processing_date': r'Data do Processamento\s+(\d{2}/\d{2}/\d{4})',  # Data do processamento
        #     # 'document_number': r'Nº do Documento\s+(\d+)',  # Número do documento
        # }

        for key, pattern in regex_dict.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_data[key] = match.group(1)
                setattr(invoice, key, match.group(1))

        # for key, value in invoice_data.items():
        #     print(f'{key}: {value}')

    def image_preprocessing(self, invoice: Invoice) -> None:
        invoice.preprocessed_image = invoice.image.copy()
        image: Image.Image = invoice.image

        # 1. Converter PIL para NumPy (necessário para OpenCV)
        image_array = np.array(image)

        # 2. Aumentar a imagem (Interpolation melhora qualidade)
        scale = 2  # Fator de aumento
        height, width = image_array.shape[:2]
        image_array = cv2.resize(image_array, (width * scale, height * scale), interpolation=cv2.INTER_CUBIC)

        # 3. Converter para escala de cinza
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # 4. Remover ruídos (Desfoque Gaussiano ou Morfologia)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # 5. Binarizar com Otsu
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 6. Aplicar morfologia (Fechamento ou Dilatação)
        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Converter de volta para PIL.Image.Image e salvar em imagens processadas
        preprocessed_image = Image.fromarray(binary)
        invoice.preprocessed_image = preprocessed_image.copy()
        # preprocessed_image.save("pagina_300dpi.png", "PNG")

    # Funcao que sera chamada fora do arquivo e juntara todas as funcoes
    def get_invoices_from_pdf(self, pdf_path: str) -> list[Invoice]:
        invoices: list[Invoice] = self.get_image_of_invoices_from_pdf(pdf_path)

        for invoice in invoices:
            self.image_preprocessing(invoice)
            self.get_data_from_invoice_image(invoice)
            print(invoice.barcode)

        return invoices