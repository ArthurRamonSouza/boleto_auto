from PIL import Image
from datetime import datetime

class Invoice:
    def __init__(self, barcode: str, type: str, company_name: str = '', creditor_cnpj: str = '', payer_name: str = '', amount: str = '1', due_date: str = '2025/02/03', invoice_number: str = ''):
        self.barcode: str = barcode
        self.type: str = type
        self.images: list[Image.Image] = []
        self.creditor_name: str = company_name
        self.creditor_cnpj: str = creditor_cnpj
        self.payer_name: str = payer_name
        self.amount: float = float(amount)
        self.due_date: datetime.date = datetime.strptime(due_date, '%Y/%m/%d').date()
        self.invoice_number: str = invoice_number
