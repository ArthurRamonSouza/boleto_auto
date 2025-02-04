from PIL import Image
from datetime import datetime

class Invoice:
    def __init__(self, barcode: str, type: str):
        self.type: str = type
        self.barcode: str = barcode
        self.images: list[Image.Image] = []
        self.preprocessed_images = []
        self.payer_name: str = ''
        self.amount: float = float('0')
        self.creditor_name: str = ''
        self.creditor_cnpj: str = ''
        self.invoice_number: str = ''
        self.due_date: datetime.date = None # datetime.strptime(due_date, '%Y/%m/%d').date()
