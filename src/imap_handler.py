from imbox import Imbox
from datetime import datetime

IMAP_SERVER: str = 'imap.gmail.com'

def get_imap_handler(email: str, password: str, unread: bool, date_gt: str, date_on: str, date_lt: str, filters: dict) -> Imbox:
    # Message kwargs filters logic
    if unread:
        filters['unread'] = True

    if date_gt:
        filters['date__gt'] = datetime.strptime(date_gt, '%Y/%m/%d').date()
    elif date_lt:
        filters['date__lt'] = datetime.strptime(date_lt, '%Y/%m/%d').date()
    elif date_on:
        filters['date__on'] = datetime.strptime(date_on, '%Y/%m/%d').date()

    return Imbox(IMAP_SERVER, username=email, password=password, ssl=True)
