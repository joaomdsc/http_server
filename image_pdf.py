# image_pdf.py - extract all the images from a pdf file

# Install with "pip install PyMuPDF"

import sys
import fitz

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <file.pdf>')
    exit()
doc = fitz.open(sys.argv[1])

for i in range(len(doc)):
    for img in doc.getPageImageList(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n >= 5:
            # CMYK: convert to RGB first
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.writePNG(f'p{i}-{xref}.png')
