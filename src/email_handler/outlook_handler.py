import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from invoice_reader import InvoiceReader, Invoice

def get_access_token(tenant_id: str, client_id: str, client_secret: str):
    try:
        token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao obter token de acesso: {e}')
        return None

def get_filters(date_gt: str, date_on: str, date_lt: str, unread_only: bool) -> str:
    filters: list[str] = ['hasAttachments eq true']

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y/%m/%d') if date_str else None
        except ValueError:
            print(f"Erro ao converter data: {date_str}")
            return None

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
        start_of_day = dt_on.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        end_of_day = dt_on.replace(hour=23, minute=59, second=59).isoformat() + 'Z'
        filters.append(f"receivedDateTime ge {start_of_day} and receivedDateTime le {end_of_day}")

    if unread_only:
        filters.append("isRead eq false")

    return " and ".join(filters)

def get_invoices(date_gt: str, date_on: str, date_lt: str, unread_only: bool):
    try:
        load_dotenv()
        CLIENT_ID: str = os.getenv('CLIENT_ID')
        CLIENT_SECRET: str = os.getenv('CLIENT_SECRET')
        TENANT_ID: str = os.getenv('TENANT_ID')
        EMAIL_ADDRESS: str = 'walison.miranda@engelmig.com.br' #os.getenv('EMAIL_ADDRESS')
        
        if not all([CLIENT_ID, CLIENT_SECRET, TENANT_ID, EMAIL_ADDRESS]):
            print('Erro: Credenciais incompletas no arquivo .env')
            return []
        
        access_token: str = get_access_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET)

        if not access_token:
            print('Erro: Não foi possível obter um token de acesso')
            return []
        
        filters: str = get_filters(date_gt, date_on, date_lt, unread_only)
        messages_url: str = f'https://graph.microsoft.com/v1.0/users/{EMAIL_ADDRESS}/messages'
        headers: dict[str] = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        params: dict[str] = {'$filter': filters, '$select': 'id,subject,hasAttachments,attachments', '$expand': 'attachments'}

        response = requests.get(messages_url, headers=headers, params=params)
        response.raise_for_status()
        messages_data = response.json()
        
        invoice_list: list[Invoice] = []
        invoice_reader: InvoiceReader = InvoiceReader()
        
        for message in messages_data.get('value', []):
            # Marking as read
            data: dict = {'isRead': True}
            mark_as_read_url: str = f"https://graph.microsoft.com/v1.0/users/{EMAIL_ADDRESS}/messages/{message['id']}"
            requests.patch(mark_as_read_url, headers=headers, json=data)
            
            for attachment in message.get('attachments', []):
                attachment_name: str = attachment['name'].lower()

                if attachment.get('contentType') == 'application/pdf' or '.pdf' in attachment_name:
                    attachment_id = attachment['id']
                    attachment_url = f"https://graph.microsoft.com/v1.0/users/{EMAIL_ADDRESS}/messages/{message['id']}/attachments/{attachment_id}/$value"
                    attachment_response = requests.get(attachment_url, headers=headers)

                    email_download_file_path: str = f'email_downloads/{attachment_name}'
                    os.makedirs(os.path.dirname(email_download_file_path), exist_ok=True)
                    
                    with open(email_download_file_path, 'wb') as file:
                        try:
                            file.write(attachment_response.content)
                            invoices: list[Invoice] = invoice_reader.get_invoices_from_pdf(email_download_file_path)
                            invoice_list.extend(invoices)

                        except Exception as e:
                            print(f'Erro ao processar fatura: {attachment_name}: {e}')
        
        return invoice_list
    except requests.exceptions.RequestException as e:
        print(f'Erro ao buscar emails: {e}')
        return []
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return []
