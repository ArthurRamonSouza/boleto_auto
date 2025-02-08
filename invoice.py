import re
import io
from PIL import Image
from datetime import datetime

class Invoice:
    """
    Represents an invoice (boleto bancário) with relevant details such as barcode,
    payer and beneficiary information, amount, due date, and image processing attributes.
    
    Attributes:
        type (str): The type of invoice (e.g., 'bank slip', 'utility bill').
        barcode (str): The barcode associated with the invoice.
        image (Image.Image): The original image of the invoice.
        preprocessed_image (Image.Image): The processed image for OCR purposes.
        payer_name (str): The name of the payer.
        payer_number (str): The identification number of the payer (e.g., CPF/CNPJ).
        amount (float): The total amount of the invoice.
        beneficiary_name (str): The name of the beneficiary.
        beneficiary_number (str): The identification number of the beneficiary (e.g., CNPJ).
        due_date (datetime.date): The due date of the invoice.
    """

    REGEX_PATTERN: re.Pattern = re.compile(r"""
        Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_name>.+?)\s*
        # CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{2}\.\d{3}\.\d{3}/\d{4}[-.]\d{2})\s*
        CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{2}\.?\d{3}\.?\d{3}/\d{4}[-.]\d{2})\s*
        Sacado:\s*(?P<payer_name>.+?)\s*
        CPF/CNPJ\ Sacado:\s*(?P<payer_number>\d{2}\.\d{3}\.\d{3}/\d{4}[-.]\d{2})\s*
        Vencimento:\s*(?P<due_date>\d{2}/\d{2}/\d{4})\s*
        Valor\ do\ Documento:\s*R\$\s*(?P<amount>[\d.,]+)\s*
    """, re.VERBOSE)
    
    

    def __init__(self, barcode: str, type: str):
        """
        Initializes an Invoice instance with the given barcode and type.

        Args:
            barcode (str): The barcode of the invoice.
            type (str): The type of invoice (e.g., 'bank slip').
        """
        self.type: str = type
        self.barcode: str = barcode
        self.image: Image.Image = None
        self.preprocessed_image: Image.Image = None
        self.payer_name: str = None
        self.payer_number: str = None
        self.amount: float = None
        self.beneficiary_name: str = None
        self.beneficiary_number: str = None
        self.due_date: datetime.date = None

    def model_text_to_invoice(self, text_form_model: str) -> None:
        match_iter = self.REGEX_PATTERN.finditer(text_form_model)
        match = next(match_iter, None)

        if match:
            # print(match.groupdict())
            data: dict = match.groupdict()

            if data.get("amount"):
                data["amount"] = float(data["amount"].split('$')[0].replace('.', '').replace(',', '.'))

            if data.get("due_date"):
                data["due_date"] = datetime.strptime(data["due_date"], "%d/%m/%Y").date()

            for key, value in data.items():
                if value:
                    print(f'{key}: {value}')
                    setattr(self, key, value)
            print('barcode: ', self.barcode)

    def save_invoice(self, download_file_path: str):
        try:
            if self.image:
                image_bytes_io = io.BytesIO()
                self.image.save(image_bytes_io, format="PNG")
                image_bytes = image_bytes_io.getvalue()

                with open(download_file_path, 'wb') as file:
                    file.write(image_bytes)

        except Exception as e:
            print('Error in method save_invoice:', e)
