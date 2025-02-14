import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from invoice_reader import InvoiceReader, Invoice

def get_access_token(tenant_id: str, client_id: str, client_secret:str ):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    token_response = requests.post(token_url, data=token_data)
    token_response_data = token_response.json()
    return token_response_data['access_token']

def refresh_token(tenant_id: str, client_id: str, client_secret:str, token: str):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'refresh_token': token
    }
    token_response = requests.post(token_url, data=token_data)
    token_response_data = token_response.json()
    return token_response_data['refresh_token']

def get_filters(date_gt: str, date_on: str, date_lt: str, unread_only: bool) -> str:
    filters = ["hasAttachments eq true"]

    def parse_date(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d") if date_str else None

    dt_gt = parse_date(date_gt)
    dt_lt = parse_date(date_lt)
    dt_on = parse_date(date_on)

    if dt_gt and dt_lt:
        filters.append(f"receivedDateTime ge {dt_gt.isoformat()}Z and receivedDateTime le {dt_lt.isoformat()}Z")
    elif dt_lt:
        filters.append(f"receivedDateTime le {dt_lt.isoformat()}Z")
    elif dt_gt:
        filters.append(f"receivedDateTime ge {dt_gt.isoformat()}Z")
    elif dt_on:
        start_of_day = dt_on.replace(hour=0, minute=0, second=0).isoformat() + "Z"
        end_of_day = dt_on.replace(hour=23, minute=59, second=59).isoformat() + "Z"
        filters.append(f"receivedDateTime ge {start_of_day} and receivedDateTime le {end_of_day}")

    if unread_only:
        filters.append("isRead eq false")

    return filters

def download_attachments(message_id: str, access_token: str, save_path: str):
    """Baixa anexos de um email específico."""
    load_dotenv()
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')

    headers = {'Authorization': f'Bearer {access_token}'}
    url = f"https://graph.microsoft.com/v1.0/users/{EMAIL_ADDRESS}/messages/{message_id}/attachments"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao buscar anexos: {response.text}")
        return []

    attachments = response.json().get('value', [])
    downloaded_files = []

    for attachment in attachments:
        attachment_name = attachment['name'].lower()
        if '.pdf' in attachment_name:
            file_path = os.path.join(save_path, attachment_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as file:
                try:
                    file.write(bytes(attachment['contentBytes'], 'utf-8'))  # Converte base64 para binário
                    downloaded_files.append(file_path)
                    print(f"Anexo salvo: {file_path}")
                except Exception as e:
                    print(f"Erro ao salvar anexo {attachment_name}: {e}")

    return downloaded_files

def get_invoices(date_gt: str, date_on: str, date_lt: str, unread_only: bool):
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    
    access_token = get_access_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Fetch emails with filters
    user_principal_name = os.getenv('EMAIL_ADDRESS')
    messages_url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/messages"
    filters: str = get_filters(date_gt, date_on, date_lt, unread_only)
    params = {
        '$filter': filters,
        '$select': 'id,subject,hasAttachments,attachments',
        '$expand': 'attachments'
    }

    messages_response = requests.get(messages_url, headers=headers, params=params)
    messages_data = messages_response.json()

    
    if 'value' in messages_data:
        invoice_reader: InvoiceReader = InvoiceReader()
        invoice_list: list[Invoice] = []

        for message in messages_data['value']:
            data = {"isRead": True}
            mark_as_readed = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/messages/{message['id']}"
            requests.patch(mark_as_readed, headers=headers, json=data)

            for attachment in message['attachments']:
                attachment_name = attachment['name'].lower()

                if attachment['contentType'] == 'application/pdf' or '.pdf' in attachment_name:
                    email_download_file_path: str = f'email_downloads/{attachment_name}'
                    os.makedirs(os.path.dirname(email_download_file_path), exist_ok=True)

                    attachment_id = attachment['id']
                    attachment_url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/messages/{message['id']}/attachments/{attachment_id}/$value"
                    attachment_response = requests.get(attachment_url, headers=headers)

                    if attachment_response.status_code == 200:
                       with open(email_download_file_path, 'wb') as file:
                        try:
                            file.write(attachment['content'].read())
                            invoices: list[Invoice] = invoice_reader.get_invoices_from_pdf(email_download_file_path)
                            invoice_list.extend(invoices)
                        except Exception as e:
                            print('Error in class main: ', e)

                    else:
                        print(f"Erro ao baixar anexo: {attachment_response.status_code}")
    return invoice_list