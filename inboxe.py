import datetime
from gui import interface_email_value, interface_password_value
from imbox import Imbox

IMAP_SERVER: str = 'imap.gmail.com'

try:
    mail= Imbox(IMAP_SERVER, username=interface_email_value, password=interface_password_value, ssl=True)
    messages = mail.messages(unread=True, raw='has:attachment', date__on=datetime.date(2025, 2, 3)) # unread=True busca apenas emails não lidos

    for uid, message in messages:
        print(f"De: {message.sent_from}")
        print(f"Assunto: {message.subject}")
        print(f"Data: {message.date}")
        print(f"Anexo: {message.attachments}")
        break

except Exception as e:
    print(f"Erro ao conectar ao servidor IMAP: {e}")
