import datetime
from invoice_reader import InvoiceReader
from models.invoice import Invoice

invoices_reader: InvoiceReader = InvoiceReader()

def test_get_invoice_Boleto_0000000056_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/Boleto_0000000056_ENGELMIG ENERGIA LTDA_924656.pdf')
    result = invoices[0]
    assert result.barcode == '13691101100000232862315000048723600000000566'
    assert result.value == 232.86
    assert result.beneficiary_name == 'LUCAS MARIANO NETO LTDA'
    assert result.beneficiary_number == '10.235.548/0001-74'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0063-00'
    assert result.due_date == datetime.date(2025, 3, 5)

def test_get_invoice_boleto5_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto5.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_BOLETOSX_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/BOLETOSX_1-119-828_002.pdf')
    result = invoices[0]
    # assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 3460
    assert result.beneficiary_name == 'DINAMICA COMERCIO DE FERRAMENTAS E EQUIP'
    assert result.beneficiary_number == '18.581.853/0001-20'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 4, 1)

def test_get_invoice_BOLETOSD_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/BOLETOSD_1-119-828_001.pdf')
    result = invoices[0]
    # assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 3460
    assert result.beneficiary_name == 'DINAMICA COMERCIO DE FERRAMENTAS E EQUIP'
    assert result.beneficiary_number == '18.581.853/0001-20'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 3, 4)

def test_get_invoice_boletos_2025_02_04T164353_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto(s) - 2025-02-04T164353.895.pdf')
    result = invoices[0]
    # assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 1332.90
    assert result.beneficiary_name == 'MARC CENTER HOTEL LTDA'
    assert result.beneficiary_number == '12.939.971/0001-80'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 19)

def test_get_invoice_boleto0_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto0.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto1_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto1.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto2_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto2.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto3_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto3.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto4_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto4.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto6_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto6.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto7_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto7.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto8_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto8.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto9_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto9.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto10_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto10.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)

def test_get_invoice_boleto11_check_result():
    invoices: list[Invoice] = invoices_reader.get_invoices_from_pdf('email_downloads/boleto11.pdf')
    result = invoices[0]
    assert result.barcode == '10497999300008347213541371000100040000399271'
    assert result.value == 8347.21
    assert result.beneficiary_name == 'MINAS GERAIS IMOVEIS'
    assert result.beneficiary_number == '57528515/0001-86'
    assert result.payer_name == 'ENGELMIG ENERGIA LTDA'
    assert result.payer_number == '21.066.139/0001-08'
    assert result.due_date == datetime.date(2025, 2, 12)