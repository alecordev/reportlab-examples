def encode(self, resource, **attr):
    """
        Export data as a PDF document

        @param resource: the resource
        @param attr: dictionary of keyword arguments, in s3_rest_controller
                     passed through from the calling controller

        @keyword request: the S3Request
        @keyword method: "read" to not include a list view when no
                         component is specified
        @keyword list_fields: fields to include in lists

        @keyword pdf_componentname: enforce this component

        @keyword pdf_groupby: how to group the results
        @keyword pdf_orderby: how to sort rows (within any level of grouping)

        @keyword pdf_callback: callback to be used rather than request

        @keyword pdf_title: the title of the report
        @keyword pdf_filename: the filename for the report

        @keyword rheader: HTML page header (override by pdf_header)
        @keyword rfooter: HTML page footer (override by pdf_footer)
        @keyword pdf_header: callback to generate the HTML header
                             (overrides rheader)
        @keyword pdf_footer: callback to generate the HTML footer,
                             or static HTML (overrides rfooter)

        @keyword pdf_header_padding: add this amount of space between
                                     the header and the body
        @keyword pdf_footer_padding: add this amount of space between
                                     the body and the footer

        @keyword pdf_hide_comments: don't show the comments in a table

        @keyword pdf_table_autogrow: Indicates that a table should grow to
                                      fill the available space. Valid values:
                                      H - Horizontal
                                      V - Vertical
                                      B - Both
        @keyword pdf_paper_alignment: Portrait (default) or Landscape
        @keyword use_colour:      True to add colour to the cells. default False

        @ToDo: Add Page Numbers in Footer:
               http://www.blog.pythonlibrary.org/2013/08/12/reportlab-how-to-add-page-numbers/
    """

    if not PILImported:
        current.session.warning = self.ERROR.PIL_ERROR
    if not reportLabImported:
        current.session.error = self.ERROR.RL_ERROR
        redirect(URL(extension=""))

    # Settings
    r = self.r = attr.get("request", None)
    self.list_fields = attr.get("list_fields")
    self.pdf_groupby = attr.get("pdf_groupby")
    self.pdf_orderby = attr.get("pdf_orderby")
    self.pdf_hide_comments = attr.get("pdf_hide_comments")
    self.table_autogrow = attr.get("pdf_table_autogrow")
    self.pdf_header_padding = attr.get("pdf_header_padding", 0)
    self.pdf_footer_padding = attr.get("pdf_footer_padding", 0)

    # Get the title & filename
    now = current.request.now.isoformat()[:19].replace("T", " ")
    title = attr.get("pdf_title")
    if title == None:
        title = "Report"
    docTitle = "%s %s" % (title, now)
    filename = attr.get("pdf_filename")
    if filename is None:
        if not isinstance(title, str):
            # Must be str not unicode
            title = title.encode("utf-8")
        filename = "%s_%s.pdf" % (title, now)
    elif len(filename) < 5 or filename[-4:] != ".pdf":
        # Add extension
        filename = "%s.pdf" % filename
    self.filename = filename

    # Get the Doc Template
    paper_size = attr.get("paper_size")
    pdf_paper_alignment = attr.get("pdf_paper_alignment", "Portrait")
    doc = EdenDocTemplate(title=docTitle,
                          paper_size=paper_size,
                          paper_alignment=pdf_paper_alignment)

    # Get the header
    header_flowable = None
    header = attr.get("pdf_header")
    if not header:
        header = attr.get("rheader")
    if header:
        header_flowable = self.get_html_flowable(header,
                                                 doc.printable_width)
        if self.pdf_header_padding:
            header_flowable.append(Spacer(1, self.pdf_header_padding))

    # Get the footer
    footer_flowable = None
    footer = attr.get("pdf_footer")
    if not footer:
        footer = attr.get("rfooter")
    if footer:
        footer_flowable = self.get_html_flowable(footer,
                                                 doc.printable_width)
        if self.pdf_footer_padding:
            footer_flowable.append(Spacer(1, self.pdf_footer_padding))

    # Build report template

    # Get data for the body of the text
    data = None
    body_flowable = None

    doc.calc_body_size(header_flowable, footer_flowable)

    callback = attr.get("pdf_callback")
    pdf_componentname = attr.get("pdf_componentname", None)
    if callback:
        # Get the document body from the callback
        body_flowable = self.get_html_flowable(callback(r),
                                               doc.printable_width)

    elif pdf_componentname:  # and resource.parent is None:
        # Enforce a particular component
        resource = current.s3db.resource(r.tablename,
                                         components=[pdf_componentname],
                                         id=r.id)
        if pdf_componentname in resource.components:
            component = resource.components[pdf_componentname]
            body_flowable = self.get_resource_flowable(component, doc)

    elif r.component or attr.get("method", "list") != "read":
        # Use the requested resource
        body_flowable = self.get_resource_flowable(resource, doc)

    styleSheet = getSampleStyleSheet()
    style = styleSheet["Normal"]
    style.fontName = self.font_name
    style.fontSize = 9
    if not body_flowable:
        body_flowable = [Paragraph("", style)]
    self.normalstyle = style

    # Build the PDF
    doc.build(header_flowable,
              body_flowable,
              footer_flowable,
              )

    # Return the generated PDF
    response = current.response
    if response:
        disposition = "attachment; filename=\"%s\"" % self.filename
        response.headers["Content-Type"] = contenttype(".pdf")
        response.headers["Content-disposition"] = disposition

    return doc.output.getvalue()
