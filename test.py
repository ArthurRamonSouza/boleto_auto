import os
from database.create_db import create_tables
from database.db_configuration import SessionLocal
from models.invoice import Invoice
from invoice_reader import InvoiceReader

download_folder_path = "/home/arthur/Documents/Visual Studio Code/freela/engelmig/boleto_auto/download_folder"

invoices_reader: InvoiceReader = InvoiceReader()
# create_tables()

# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto0.pdf')
# Beneficiário ou Cedente: ACME Telecomunicações Ltda
# CPF/CNPJ do Beneficiário ou Cedente: 074.064.502/0001-12
# Sacado: AME Telecomunicações Ltda
# CPF/CNPJ Sacado: 074.064.502/0001-12
# Vencimento: 04/12/2017
# Valor do Documento: R$ 9,90

# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto1.pdf')
# Beneficiário ou Cedente: Conselho Regional de Enfermagem Sergipe
# CPF/CNPJ do Beneficiário ou Cedente: 34/03/2015
# Sacado: GUILHERME DIANGELIS GOMES
# CPF/CNPJ Sacado: 49092-540
# Vencimento: 34/03/2015
# Valor do Documento: R$ 315,20
# Error to create Invoice from: email_downloads/boleto1.pdf
# Tempo de Processamento Total: 109.19 segundos

# 1
# beneficiary_name: SACFLEX LTDA
# beneficiary_number: 50.266.341/0001-81
# payer_name: ENGELMIG ELETRICA LTDA
# payer_number: 21.066.139/0002-99
# due_date: 2025-02-15
# amount: 1600.0

# 2
# beneficiary_name: QUERO CONSTRUIR LTDA
# beneficiary_number: 40.811.826/0001-55
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.066.139/0012-60
# due_date: 2025-02-15
# amount: 785.3

# 3
# beneficiary_name: VÓLUS INSTITUIÇÃO DE PAGAMENTO LTDA
# beneficiary_number: 03.817.702/0001-50
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.066.139/0004-50
# due_date: 2025-02-15
# amount: 20891.65

# 4
# beneficiary_name: PEDRA BONITA PREC HOTEL LTDA
# beneficiary_number: 04.165.360/0001-02
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.066.139/0023-13
# due_date: 2025-02-15
# amount: 5829.4

# 5
# Pulou
# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto5.pdf')
# beneficiary_name: MINAS GERAIS IMOVEIS
# beneficiary_number: 57528515/0001-66
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.008.139/0001-08
# due_date: 2025-02-15
# amount: 8347.21
# barcode:  10497999300008347213541371000100040000399271
# Tempo de Processamento Total: 49.35 segundos

# 6
# Pulou

# 7
# Falha na leitura

# 8
# Pulou

# 9
# beneficiary_name: S.W.A.T MANUTENCAO E COMERCIO DE PECAS LTDA
# beneficiary_number: 37.175.816/0001-00
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.066.139/0006-12
# due_date: 2025-02-15
# amount: 2978.0

# 10
# beneficiary_name: BRASFER COM MANGUEIRAS E SERVICOS LTDA
# beneficiary_number: 07.875.801/0001-40
# payer_name: ENGELMIG ELETRICA LTDA
# payer_number: 21.066.139/0004-50
# due_date: 2025-02-15
# amount: 765.6

# 11
# beneficiary_name: ENGELMIG ENERGIA LTDA
# beneficiary_number: 21.066.139/0006-12
# payer_name: KAWAL EPIS SOLDAS ABRASIVOS MAQUINAS E FERRAMENTAS LTDA
# payer_number: 48.898.541/0001-05
# due_date: 2025-02-15
# amount: 464.3

# Tempo de Processamento Total: 411.40 segundos

invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto5.pdf') #ppi950
# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/BOLETOSD_1-119-828_001.pdf')
# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/doc16732420250204174241.pdf')

# with SessionLocal() as session:
#     try:
#         for invoice in invoices:
#             download_file_path: str = f'{download_folder_path}/{invoice.due_date} - {invoice.amount} - {invoice.beneficiary_name}.png'
#             os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
#             invoice.save_as_file(download_file_path)
#             invoice.save_to_db(session)
        
#     except Exception as e:
#         print(f"Error to save in database: {e}")