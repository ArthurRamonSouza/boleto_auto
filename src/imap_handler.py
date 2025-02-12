from imbox import Imbox
from datetime import datetime

IMAP_SERVER: str = 'imap.gmail.com'

def get_imap_handler(email: str, password: str, unread: bool, date_gt: str, date_on: str, date_lt: str, filters: dict) -> Imbox:
    """
    Creates an IMAP handler to interact with an email inbox.

    This function establishes a connection to an IMAP server using the provided credentials (email and password),
    applying the specified filters for unread status and date range, and returns an Imbox instance to interact with the mailbox.

    Args:
        email (str): The email address to authenticate with the IMAP server.
        password (str): The password or application-specific password for the email account.
        unread (bool): If True, filters for unread messages.
        date_gt (str): A string representing a date in the format 'YYYY/MM/DD'. If provided, filters messages sent after this date.
        date_on (str): A string representing a date in the format 'YYYY/MM/DD'. If provided, filters messages sent on this date.
        date_lt (str): A string representing a date in the format 'YYYY/MM/DD'. If provided, filters messages sent before this date.
        filters (dict): Additional filters to apply when fetching messages. The dictionary will be updated based on the provided arguments.

    Returns:
        Imbox: An Imbox instance connected to the IMAP server with the specified filters applied.

    Example:
        email = "user@example.com"
        password = "password123"
        unread = True
        date_gt = "2025/01/01"
        filters = {}
        
        handler = get_imap_handler(email, password, unread, date_gt, None, None, filters)
        print(handler.messages())  # Fetches the filtered messages
    """
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
