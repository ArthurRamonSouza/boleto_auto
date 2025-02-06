from imap_handler import get_imap_handler, Imbox
from invoice_reader import InvoiceReader, Invoice
from gui import root, get_download_folder_path, get_filters, get_login

root.mainloop()
email, password = get_login()
download_folder_path = get_download_folder_path()
date_gt, date_on, date_lt, unread_only = get_filters()

filters: dict = {'raw': 'has:attachment'}
email_halder: Imbox = get_imap_handler(email, password, unread_only, date_gt, date_on, date_lt, filters)
messages = email_halder.messages(**filters)

invoice_reader: InvoiceReader = InvoiceReader()

for (uuid, message) in messages:
    if len(message.attachments) > 0:
        for attachment in message.attachments:
            attachment_file: str = attachment['filename']

            if '.pdf' in attachment_file:
                download_file_path: str = f'{download_folder_path}/{attachment_file}'

                with open(download_file_path, 'wb') as file:
                    file.write(attachment['content'].read())

                    try:
                        invoice_reader.get_invoices_from_pdf(download_file_path)
                    except Exception as e:
                        print('Erro na classe main: ', e)


