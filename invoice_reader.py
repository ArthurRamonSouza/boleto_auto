import os
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

    # Pega todas as imagens de um pdf, o codigo de barras e o tipo
    def get_invoices_images_from_pdf(self, pdf_path: str = '') -> list[Invoice]:
        try:
            pdf_images: list[Image.Image] = convert_from_path(pdf_path, 200)
            invoice_list: list[Invoice] = []
            invoice_img_buffer: list[Image.Image] = []

            # Para cada imagem no pdf
            for image in pdf_images:
                    invoice_img_buffer.append(image)
                    decoded_images: list = decode(image)

                    if not decoded_images:
                        print(f"There wasn't barcodes in the pdf")

                    else:
                        # Captura todas as imagens relativas a um boleto, o codigo de barras e o tipo
                        for barcode in decoded_images:
                            if barcode.data != '' and barcode.type == 'I25':
                                invoice: Invoice = Invoice(barcode.data.decode('utf-8'), 'I25')
                                invoice.images = invoice_img_buffer.copy()
                                invoice_list.append(invoice)
                        # Limpa o buffer
                        invoice_img_buffer.clear()
                    
            return invoice_list
        except Exception as e:
            print(f'Error while decoding the pdf: {e}')
            

    # Faz a busca por texto nas imagens do boleto
    def get_data_from_invoice_images(self, invoice: Invoice) -> None:
        text = pytesseract.image_to_string(invoice.images[0], lang="por")
        # print(text)

        dados = {}

        regex_dict = {
            "banco": r"(\bBradesco\b|\bItaú\b|\bCaixa\b|\bSantander\b|\bBanco do Brasil\b)",
            # "codigo_barras": r"(\d{5}\.\d{5} \d{5}\.\d{6} \d \d{14})",
            "beneficiario": r"Beneficiário\s+(.*?)\s+-\s+CNPJ",
            "cnpj_beneficiario": r"CNPJ\s+([\d\.\-\/]+)",
            "sacador": r"Sacador/Avalista\s+(.*?)\s+-\s+\d{2,3}\.\d{3}\.\d{3}\/\d{4}-\d{2}",
            "cnpj_sacador": r"Sacador/Avalista\s+.*\s+-\s+([\d\.\-\/]+)",
            "pagador": r"Pagador\s+(.*?)\s+-\s+\d{3}\.\d{3}\.\d{3}-\d{2}",
            "cpf_pagador": r"Pagador.*?(\d{3}\.\d{3}\.\d{3}-\d{2})",
            "vencimento": r"Data de Vencimento\s+(\d{2}/\d{2}/\d{4})",
            "valor": r"R\$\s*([\d,]+)",
            # "codigo_cedente": r"Agência / Código do Cedente\s+([\d\/\-]+)",
            "nosso_numero": r"Nosso Número\s*.(\d{2}\/\d{11}-\d{1})"
        }

        for chave, padrao in regex_dict.items():
            match = re.search(padrao, text, re.IGNORECASE)
            if match:
                dados[chave] = match.group(1)

        for chave, valor in dados.items():
            print(f"{chave}: {valor}")

    def image_preprocessing(self, invoice: Invoice) -> None:
        invoice.preprocessed_images = invoice.images.copy()
        images: list[Image.Image] = invoice.images

        for image in images:
            image_array = np.array(image)

            # Se a imagem for colorida, converter para escala de cinza
            if len(image_array.shape) == 3:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

            # Aplicar binarização (Thresholding)
            _, image_array = cv2.threshold(image_array, 150, 255, cv2.THRESH_BINARY)

            # Remover ruído com morfologia (Fechamento)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            image_array = cv2.morphologyEx(image_array, cv2.MORPH_CLOSE, kernel)

            # Aplicar filtro de nitidez
            kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            image_array = cv2.filter2D(image_array, -1, kernel_sharpen)

            # Aumentar tamanho da imagem (melhora a detecção de caracteres pequenos)
            image_array = cv2.resize(image_array, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            # Converter de volta para PIL.Image.Image e salvar em imagens processadas
            image = Image.fromarray(image_array)
            invoice.preprocessed_images.append(image)

    # Funcao que sera chamada fora do arquivo e juntara todas as funcoes
    def get_invoices_from_pdf(self, pdf_path: str) -> list[Invoice]:
        invoices: list[Invoice] = self.get_invoices_images_from_pdf(pdf_path)

        for invoice in invoices:
            self.image_preprocessing(invoice)
            self.get_data_from_invoice_images(invoice)

        return invoices