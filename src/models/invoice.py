import re
import io
from PIL import Image
from datetime import datetime

from database.db_configuration import Base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, Date, LargeBinary


class Invoice(Base):
    __tablename__ = "boletos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    barcode_type = Column(String(50))
    barcode = Column(String(100), unique=True, nullable=False)
    payer_name = Column(String(144))
    payer_number = Column(String(50))
    value = Column(Float)
    beneficiary_name = Column(String(144))
    beneficiary_number = Column(String(50))
    due_date = Column(Date)
    image = Column(LargeBinary)
    
    REGEX_PATTERN: re.Pattern = re.compile(r"""
        Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_name>[\w\s]+?)\s*
        # CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{2}\.\d{3}\.\d{3}/\d{4}[-.]\d{2})\s*
        # CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{2}\.?\d{3}\.?\d{3}/\d{4}[-.]\d{2})\s*
        CPF/CNPJ\ do\ Beneficiário\ ou\ Cedente:\s*(?P<beneficiary_number>\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/\d{4}[-.]?\d{2})\s*
        Sacado:\s*(?P<payer_name>.+?)\s*
        # CPF/CNPJ\ Sacado:\s*(?P<payer_number>\d{2}\.\d{3}\.\d{3}/\d{4}[-.]\d{2})\s*
        CPF/CNPJ\ Sacado:\s*(?P<payer_number>\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}/\d{4}[-.]?\d{2})\s*
        Vencimento:\s*(?P<due_date>\d{2}/\d{2}/\d{4})\s*
        Valor\ do\ Documento:\s*R\$\s*(?P<value>[\d.,]+)\s*
    """, re.VERBOSE)    

    def __init__(self, barcode: str, barcode_type: str, 
                payer_name: str = None, 
                payer_number: str = None,
                value: str = None,
                beneficiary_name: str = None,
                beneficiary_number: str = None,
                due_date: any = None,
                image: any = None
                ):
        self.barcode_type: str = barcode_type
        self.barcode: str = barcode
        self.image: Image.Image = image
        self.preprocessed_image: Image.Image = None
        self.payer_name: str = payer_name
        self.payer_number: str = payer_number
        self.value: float = value
        self.beneficiary_name: str = beneficiary_name
        self.beneficiary_number: str = beneficiary_number
        self.due_date: datetime.date = due_date

    def model_text_to_invoice(self, text_form_model: str) -> None:
        match_iter = self.REGEX_PATTERN.finditer(text_form_model)
        match = next(match_iter, None)

        if match:
            data: dict = match.groupdict()

            if data.get("beneficiary_name"):
                data["beneficiary_name"] = data["beneficiary_name"][:-1] if data["beneficiary_name"][-1] == '.' else data["beneficiary_name"] 

            if data.get("payer_name"):
                data["payer_name"] = data["payer_name"][:-1] if data["payer_name"][-1] == '.' else data["payer_name"] 

            if data.get("beneficiary_number"):
                beneficiary_number_without_hyphen = re.sub(r'-(?=\d+$)', '.', data["beneficiary_number"])
                data["beneficiary_number"] = re.sub(r'\.(?=[^\.]+$)', '-', beneficiary_number_without_hyphen)

            if data.get("payer_number"):
                payer_number_without_hyphen = re.sub(r'-(?=\d+$)', '.', data["payer_number"])
                data["payer_number"] = re.sub(r'\.(?=[^\.]+$)', '-', payer_number_without_hyphen)

            if data.get("value"):
                data["value"] = float(data["value"].split('$')[0].replace('.', '').replace(',', '.'))

            if data.get("due_date"):
                data["due_date"] = datetime.strptime(data["due_date"], "%d/%m/%Y").date()
            
            check_value()

            for key, value in data.items():
                if value:
                    setattr(self, key, value)

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
                barcode_type=self.barcode_type,
                barcode=self.barcode,
                payer_name=self.payer_name,
                payer_number=self.payer_number,
                value=self.value,
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
    
    def check_value(self):
        barcode_value_str: str = self.barcode[-10:]
        barcode_value: float = float(barcode_value_str)

        if self.value != barcode_value:
            self.value = barcode_value
            print("Possível fraude detectada. Confirme o valor do boleto e o código de barra.")
