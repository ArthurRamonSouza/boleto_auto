from PIL import Image
from datetime import datetime

class Invoice:
    """
    Represents an invoice (boleto bancário) with relevant details such as barcode,
    payer and beneficiary information, amount, due date, and image processing attributes.
    
    Attributes:
        type (str): The type of invoice (e.g., 'bank slip', 'utility bill').
        barcode (str): The barcode associated with the invoice.
        invoice_number (str): The unique invoice number.
        image (Image.Image): The original image of the invoice.
        preprocessed_image (Image.Image): The processed image for OCR purposes.
        payer_name (str): The name of the payer.
        payer_number (str): The identification number of the payer (e.g., CPF/CNPJ).
        amount (float): The total amount of the invoice.
        beneficiary_name (str): The name of the beneficiary.
        beneficiary_number (str): The identification number of the beneficiary (e.g., CNPJ).
        guantor_name (str): The name of the guarantor (if applicable).
        guantor_number (str): The identification number of the guarantor (e.g., CPF/CNPJ).
        due_date (datetime.date): The due date of the invoice.
    """
    def __init__(self, barcode: str, type: str):
        """
        Initializes an Invoice instance with the given barcode and type.

        Args:
            barcode (str): The barcode of the invoice.
            type (str): The type of invoice (e.g., 'bank slip').
        """
        self.type: str = type
        self.barcode: str = barcode
        self.invoice_number: str = ''
        self.image: Image.Image = None
        self.preprocessed_image: Image.Image = None
        self.payer_name: str = ''
        self.payer_number: str = ''
        self.amount: float = float('0')
        self.beneficiary_name: str = ''
        self.beneficiary_number: str = ''
        self.guantor_name: str = ''
        self.guantor_number: str = ''
        self.due_date: datetime.date = None  # Expected to be set later
