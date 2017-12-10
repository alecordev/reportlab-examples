from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

import io


buf = io.BytesIO()

# Setup the document with paper size and margins
doc = SimpleDocTemplate(
    buf,
    rightMargin=inch / 2,
    leftMargin=inch / 2,
    topMargin=inch / 2,
    bottomMargin=inch / 2,
    pagesize=letter,
)

# Styling paragraphs
styles = getSampleStyleSheet()

# Write things on the document
paragraphs = []
paragraphs.append(
    Paragraph('This is a paragraph', styles['Normal']))
paragraphs.append(
    Paragraph('This is another paragraph', styles['Normal']))
doc.build(paragraphs)

# Write the PDF to a file
with open('test.pdf', 'bw') as fd:
    fd.write(buf.getvalue())
