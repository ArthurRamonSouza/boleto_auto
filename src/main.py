import os
import gui
from email import outlook
from email import gmail_handler
from models.invoice import Invoice
from database.create_db import create_tables
from database.db_configuration import SessionLocal

def main():
    gui.root.mainloop()

    create_tables()

    email, password = gui.get_interface_login()
    download_folder_path = gui.get_interface_download_folder_path()
    date_gt, date_on, date_lt, unread_only = gui.get_interface_filters()

    invoice_list: list[Invoice] = []

    if os.getenv('EMAIL').lower() == 'gmail':
        invoice_list = gmail_handler.get_invoices(email, password, unread_only, date_gt, date_on, date_lt)
    else:
        invoice_list = outlook.get_invoices()

    save_invoices_into_db_and_file_explorer(invoice_list, download_folder_path)

def save_invoices_into_db_and_file_explorer(invoice_list: list[Invoice], download_folder_path: str):
    with SessionLocal() as session:
        for invoice in invoice_list:
            try:
                download_file_path = f'{download_folder_path}/{invoice.due_date} - {invoice.value} - {invoice.beneficiary_name}.png'
                os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

                invoice.save_as_file(download_file_path)
                invoice.save_to_db(session)

                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Error saving invoice {invoice.barcode}: {e}")

if __name__ == "__main__":
    main()