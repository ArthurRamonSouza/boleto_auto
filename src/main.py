import os
import gui
from database.create_db import create_tables
from imap_handler import get_imap_handler, Imbox
from invoice_reader import InvoiceReader, Invoice
from database.db_configuration import SessionLocal

gui.root.mainloop()

create_tables()

email, password = gui.get_interface_login()
download_folder_path = gui.get_interface_download_folder_path()
date_gt, date_on, date_lt, unread_only = gui.get_interface_filters()

filters: dict = {'raw': 'has:attachment'}
email_halder: Imbox = get_imap_handler(email, password, unread_only, date_gt, date_on, date_lt, filters)
messages = email_halder.messages(**filters)

invoice_reader: InvoiceReader = InvoiceReader()
invoice_list: list[Invoice] = []

for (uuid, message) in messages:
    email_halder.mark_seen(uuid)
    
    if len(message.attachments) > 0:
        for attachment in message.attachments:
            attachment_file: str = attachment['filename'].lower()

            if '.pdf' in attachment_file:
                email_download_file_path: str = f'email_downloads/{attachment_file}'
                os.makedirs(os.path.dirname(email_download_file_path), exist_ok=True)

                with open(email_download_file_path, 'wb') as file:
                    try:
                        file.write(attachment['content'].read())
                        invoices: list[Invoice] = invoice_reader.get_invoices_from_pdf(email_download_file_path)
                        invoice_list.extend(invoices)
                    except Exception as e:
                        print('Error in class main: ', e)
                        
with SessionLocal() as session:
    for invoice in invoice_list:
        try:
            download_file_path = f'{download_folder_path}/{invoice.due_date} - {invoice.amount} - {invoice.beneficiary_name}.png'
            os.makedirs(os.path.dirname(download_file_path), exist_ok=True)

            invoice.save_as_file(download_file_path)
            invoice.save_to_db(session)

            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error saving invoice {invoice.barcode}: {e}")

print("Finished processing invoices.")
