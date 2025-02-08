import cv2
import pytesseract
import numpy as np
from PIL import Image
from invoice import Invoice
from pyzbar.pyzbar import decode
from model import extract_invoice_data
from pdf2image import convert_from_path

class InvoiceReader:

    def __init__(self):
        pass

    # Pega toda a imagem de um boleto no pdf, o codigo de barras e o tipo
    def __get_image_of_invoices_from_pdf(self, pdf_path: str = '', ppi: int = 300) -> list[Invoice]:
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

    # Retorna texto presente na imagen do boleto
    def __get_text_from_invoice_image(self, invoice: Invoice) -> str:
        try:
            return pytesseract.image_to_string(invoice.image, lang='por', config='--psm 6')
        except Exception as e:
            print('Could not read current image data. Error: ', e)

    def __image_preprocessing(self, invoice: Invoice) -> None:
        invoice.preprocessed_image = invoice.image.copy()
        image: Image.Image = invoice.image

        # 1. Converter PIL para NumPy (necessário para OpenCV)
        image_array = np.array(image)

        scale = 2
        height, width = image_array.shape[:2]
        image_array = cv2.resize(image_array, (width * scale, height * scale), interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        kernel = np.ones((2,2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Converter de volta para PIL.Image.Image e salvar em imagens processadas
        preprocessed_image = Image.fromarray(binary)
        invoice.preprocessed_image = preprocessed_image.copy()
        preprocessed_image.save("pagina_300dpi.png", "PNG")

    def get_invoices_from_pdf(self, pdf_path: str) -> list[Invoice]:
        invoices: list[Invoice] = self.__get_image_of_invoices_from_pdf(pdf_path)

        for invoice in invoices:
            self.__image_preprocessing(invoice)
            invoice_text: str = self.__get_text_from_invoice_image(invoice)
            model_return: str = extract_invoice_data(invoice_text)
            print(model_return)
            invoice.model_text_to_invoice(model_return)

            missing_fields: list = [attr for attr in vars(invoice) if getattr(invoice, attr) is None]

            attempts: int = 0
            while len(missing_fields) > 0 and attempts < 2:
                print('Missing values: ', missing_fields)
                self.__image_preprocessing(invoice)
                invoice_text: str = self.__get_text_from_invoice_image(invoice)
                model_return: str = extract_invoice_data(invoice_text)
                print(model_return)
                invoice.model_text_to_invoice(model_return)

                missing_fields = [attr for attr in vars(invoice) if getattr(invoice, attr) is None]
                attempts += 1

            if len(missing_fields) > 0:
                print(f"Error to create Invoice from: {pdf_path}")
                invoices.remove(invoice)
        return invoices