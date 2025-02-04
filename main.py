from gui import root

import pytesseract
from PIL import Image

from invoice import Invoice
from invoice_reader import InvoiceReader

reader = InvoiceReader()
invoices: list[Invoice] = reader.get_invoice_images_from_pdf('/home/arthur/Documents/Visual Studio Code/freela/engelmig/boleto_auto/boleto0.pdf')
print(invoices[0].images)
print(invoices[0].barcode)

img = invoices[0].images[0]
text = pytesseract.image_to_string(img, lang="por")
print("Texto extraído:", text)

# root.mainloop()

