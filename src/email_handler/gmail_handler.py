import os
from imbox import Imbox
from datetime import datetime
from invoice_reader import InvoiceReader, Invoice

def get_gmail_handler(email: str, password: str, unread: bool, date_gt: str, date_on: str, date_lt: str, filters: dict) -> Imbox:
    # Message kwargs filters logic
    if unread:
        filters['unread'] = True

    if date_gt:
        filters['date__gt'] = datetime.strptime(date_gt, '%Y/%m/%d').date()
    elif date_lt:
        filters['date__lt'] = datetime.strptime(date_lt, '%Y/%m/%d').date()
    elif date_on:
        filters['date__on'] = datetime.strptime(date_on, '%Y/%m/%d').date()

    return Imbox('imap.gmail.com', username=email, password=password, ssl=True)

def get_invoices(email: str, password: str, unread_only: bool, date_gt: str, date_on: str, date_lt: str) -> list[Invoice]:
    filters: dict = {'raw': 'has:attachment'}
    email_halder: Imbox = get_gmail_handler(email, password, unread_only, date_gt, date_on, date_lt, filters)
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
    return invoice_list