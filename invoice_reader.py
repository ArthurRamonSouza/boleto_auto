import os
from PIL import Image
from invoice import Invoice
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path

class InvoiceReader:

    def __init__(self):
        pass

    # Pega todas as imagens de um pdf, o codigo de barras e o tipo
    def get_invoice_images_from_pdf(self, pdf_path: str = '') -> list[Invoice]:
        try:
            pdf_images: list[Image.Image] = convert_from_path(pdf_path, 500)
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
                    
        except Exception as e:
            print(f'Error while decoding the pdf: {e}')
            
        return invoice_list

    # Faz a busca por texto nas imagens do boleto
    def get_data_from_invoice_images(self, invoice: Invoice) -> None:
        pass

    def image_preprocessing():
        pass
    #Funcao que sera chamada fora do arquivo e juntara todas as funcoes
    def get_invoices_from_pdf():
        pass