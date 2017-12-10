from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    SimpleDocTemplate,
    Frame,
    Table,
    TableStyle,
    Paragraph,
)

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet, CenterStyle
from reportlab.lib.units import cm, inch


def do_print_out(recipe, page_size, filename=None):
    """do_print_out(recipe,page_size,filename=None)

    This makes makes a pdf out of the recipe opject on the size paper requested.
    recipe is a Recipe object.
    page_size is (height,width).
    If no file name is provided the automatic name generator is used. 
    See NoteCard class for more details.
    """

    try:
        page_size = tuple(page_size)
    except TypeError:
        print("size needs to be a iterable")
    else:
        (doc, columns) = get_doc(recipe.Title,
                                 recipe.Author,
                                 page_size,
                                 filename=filename)
        styles = getSampleStyleSheet()
        btext = "\xe2\x80\xa2"
        n_style = styles["Normal"]
        c_style = CenterStyle()
        ing_style = IngredientsStyle()
        Story = []
        spacer = Spacer(1, 0.05 * inch)

        # Header block
        Story.append(Paragraph(recipe.Title, styles["title"]))
        # string mod works inside vars as well. s="%s"; s%(foo,)
        time_s = "Prep Time: %s, Cook Time: %s"
        times = time_s % (recipe.Preptime, recipe.Cooktime)
        Story.append(Paragraph(times, c_style))
        Story.append(spacer)

        # ingredients block
        table = recipe.ingredients_columns(columns)
        table = [[Paragraph(y, ing_style, bulletText=btext)
                  for y in x] for x in table]
        table = Table(table)
        pad = 0
        # make the table take up less space.
        table.setStyle(TableStyle([("BOTTOMPADDING", (0, 0), (-1, -1), pad),
                                   ("TOPPADDING", (0, 0), (-1, -1), pad),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                                   ("LEFTPADDING", (0, 0), (-1, -1), pad)]))
        Story.append(table)
        Story.append(spacer)

        # directions block
        p = [Paragraph(x, n_style) for x in recipe.instructions_paragraph]
        # fix making more than one printout per python instance.
        # otherwise the directions count overall not per printout.
        p += [Paragraph("<seqreset>", n_style)]
        Story.append(KeepTogether(p))
        doc.build(Story)
