from gui import root
from invoice import Invoice
from invoice_reader import InvoiceReader

reader = InvoiceReader()
reader.get_invoices_from_pdf('/home/arthur/Documents/Visual Studio Code/freela/engelmig/boleto_auto/boleto0.pdf')
# root.mainloop()

