import os
import time
from invoice import Invoice
from gui import get_interface_download_folder_path
from invoice_reader import InvoiceReader

start_time = time.time()
download_folder_path = "/home/arthur/Documents/Visual Studio Code/freela/engelmig/boleto_auto/download_folder"

invoices_reader: InvoiceReader = InvoiceReader()
# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/Boleto_0000000056_ENGELMIG ENERGIA LTDA_924656.pdf')
# beneficiary_name: LUCAS MARIANO NETO LTDA
# beneficiary_number: 10.235.548/0001-74
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.066.139/0063-00
# due_date: 2025-03-05
# amount: 232.86
# Tempo de Processamento Total: 27.45 segundos

# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto(s) - 2025-02-04T164353.895.pdf')
# beneficiary_name: MARC CENTER HOTEL LTDA
# beneficiary_number: 12.939.971/0001-80
# payer_name: ENGELMIG ENERGIA LTDA
# payer_number: 21.066.139/0001-08
# due_date: 2025-02-19
# amount: 1332.9
# Tempo de Processamento Total: 35.70 segundos

# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/BOLETOSD_1-119-828_001.pdf')
# beneficiary_name: DINAMICA COMERCIO DE FERRAMENTAS E EQUIP
# beneficiary_number: 18.581.853/0001.20
# payer_name: ENGELMIG ENERGIA LTDA.
# payer_number: 21.066.139/0001.08
# due_date: 2025-02-04
# amount: 3460.0
# Tempo de Processamento Total: 36.95 segundos

# invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/BOLETOSX_1-119-828_002.pdf')
# beneficiary_name: DINAMICA COMERCIO DE FERRAMENTAS E EQUIP
# beneficiary_number: 18.581.853/0001.20
# payer_name: ENGELMIG ENERGIA LTDA.
# payer_number: 21.066.139/0001.08
# due_date: 2025-04-01
# amount: 3460.0
# Tempo de Processamento Total: 33.26 segundos

invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/doc16732420250204174241.pdf')
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

end_time = time.time()
elapsed_time = end_time - start_time

for invoice in invoices:
    download_file_path: str = f'{download_folder_path}/{invoice.due_date} - {invoice.amount} - {invoice.beneficiary_name}.png'
    os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
    invoice.save_invoice(download_file_path)

print(f"Tempo de Processamento Total: {elapsed_time:.2f} segundos")