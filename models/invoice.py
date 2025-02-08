import re
import io
from PIL import Image
from datetime import datetime

from db_configuration import Base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, Date, LargeBinary


class Invoice(Base):
    _tablename__ = "boletos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50))
    barcode = Column(String(100), unique=True, nullable=False)
    payer_name = Column(String(144))
    payer_number = Column(String(50))
    amount = Column(Float)
    beneficiary_name = Column(String(144))
    beneficiary_number = Column(String(50))
    due_date = Column(Date)
    image = Column(LargeBinary)
    
    REGEX_PATTERN: re.Pattern = re.compile(r"""
        Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_name>.+?)\s*
        # CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{2}\.\d{3}\.\d{3}/\d{4}[-.]\d{2})\s*
        # CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{2}\.?\d{3}\.?\d{3}/\d{4}[-.]\d{2})\s*
        CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<payer_number>\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/\d{4}-?\d{2})\s*
        Sacado:\s*(?P<payer_name>.+?)\s*
        # CPF/CNPJ\ Sacado:\s*(?P<payer_number>\d{2}\.\d{3}\.\d{3}/\d{4}[-.]\d{2})\s*
        CPF/CNPJ\ Sacado:\s*(?P<payer_number>\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/\d{4}-?\d{2})\s*
        Vencimento:\s*(?P<due_date>\d{2}/\d{2}/\d{4})\s*
        Valor\ do\ Documento:\s*R\$\s*(?P<amount>[\d.,]+)\s*
    """, re.VERBOSE)    

    def __init__(self, barcode: str, invoice_type: str):
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

    def save_as_file(self, download_file_path: str):
        try:
            if self.image:
                image_bytes_io = io.BytesIO()
                self.image.save(image_bytes_io, format="PNG")
                image_bytes = image_bytes_io.getvalue()

                with open(download_file_path, 'wb') as file:
                    file.write(image_bytes)

        except Exception as e:
            print('Error in method save_invoice:', e)

    def save_to_db(self, session: Session):
        try:
            image_bytes = None
            if self.image:
                image_bytes_io = io.BytesIO()
                self.image.save(image_bytes_io, format="PNG")
                image_bytes = image_bytes_io.getvalue()

            new_invoice = Invoice(
                type=self.type,
                barcode=self.barcode,
                payer_name=self.payer_name,
                payer_number=self.payer_number,
                amount=self.amount,
                beneficiary_name=self.beneficiary_name,
                beneficiary_number=self.beneficiary_number,
                due_date=self.due_date,
                image=image_bytes
            )

            session.add(new_invoice)
            session.commit()
            print(f"Invoice {self.barcode} saved successfully!")

        except Exception as e:
            session.rollback()
            print(f"Error saving invoice: {e}")

        finally:
            session.close()