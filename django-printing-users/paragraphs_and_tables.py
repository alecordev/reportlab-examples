from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings

# Register Fonts
pdfmetrics.registerFont(
    TTFont('Arial', settings.STATIC_ROOT + 'fonts/arial.ttf'))
pdfmetrics.registerFont(
    TTFont('Arial-Bold', settings.STATIC_ROOT + 'fonts/arialbd.ttf'))

# A large collection of style sheets pre-made for us
styles = getSampleStyleSheet()
# Our Custom Style
styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))


def print_users_paragraph(self):
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
    styles.add(ParagraphStyle(name='RightAlign', fontName='Arial' alignment=TA_RIGHT))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    users = User.objects.all()
    elements.append(Paragraph('My User Names', styles['RightAlign']))
    # elements.append(Paragraph('<font name="Arial-Bold" color="red">My</font> User Names<img src="smiley.jpg" height="5">', styles['RightAlign']))
    for i, user in enumerate(users):
        elements.append(Paragraph(user.get_full_name(), styles['Normal']))

    doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer,
                canvasmaker=NumberedCanvas)

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def print_users_table(self):
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
    styles.add(ParagraphStyle(name='RightAlign', fontName='Arial' alignment=TA_RIGHT))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    users = User.objects.all()
    elements.append(Paragraph('My User Names', styles['RightAlign']))

    # Need a place to store our table rows
    table_data = []
    for i, user in enumerate(users):
        # Add a row to the table
        table_data.append([user.get_full_name(), user.username, user.last_login]))
    # Create the table
    user_table=Table(table_data, colWidths = [doc.width / 3.0] * 3)
    user_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
    elements.append(user_table)
    doc.build(elements, onFirstPage = self._header_footer, onLaterPages = self._header_footer,
                canvasmaker = NumberedCanvas)

    # Get the value of the BytesIO buffer and write it to the response.
    pdf=buffer.getvalue()
    buffer.close()
    return pdf
