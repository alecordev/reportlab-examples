from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    SimpleDocTemplate,
    Frame,
    Table,
    TableStyle,
    Paragraph,
)

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch

styles = getSampleStyleSheet()


def go():
    doc = SimpleDocTemplate("phello.pdf")
    doc.pagesize = (6 * inch, 4 * inch)
    doc.leftMargin = 0.25 * inch
    doc.bottommargin = 0.25 * inch
    # doc.height=3.75*inch
    # doc.width=5.75*inch
    doc.height = 4 * inch
    doc.width = 6 * inch
    Story = []
    style = styles["Normal"]
    for i in range(3):
        bogustext = ("This is Paragraph number %s. " % i) * 2
        p = Paragraph(bogustext, style)
        # p = Paragraph(bogustext)
        Story.append(p)
        # Story.append(Spacer(1,0.2*inch))
    l = []
    for x in range(3):
        l.append(["row%i col1" % x, "row%i col2" % i])
    Story.append(Table(l))
    Story.append(Paragraph("Hello", styles["Title"]))
    # Story.append(Paragraph("Hello"))
    #doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    doc.build(Story)


go()
