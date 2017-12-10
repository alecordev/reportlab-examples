from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User


def print_users(self):
    buffer = self.buffer
    doc = SimpleDocTemplate(buffer,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72,
                            pagesize=self.pagesize)

    # Our container for 'Flowable' objects
    elements = []

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    users = User.objects.all()
    elements.append(Paragraph('My User Names', styles['Heading1']))
    for i, user in enumerate(users):
        elements.append(Paragraph(user.get_full_name(), styles['Normal']))

    # doc.build(elements)
    doc.build(elements,
              onFirstPage=self._header_footer,
              onLaterPages=self._header_footer,
              canvasmaker=NumberedCanvas)

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
