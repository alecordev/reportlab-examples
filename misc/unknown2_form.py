def OCRPDFManager(self):
    """
        Produces OCR Compatible PDF forms
    """

    T = current.T
    s3ocr_root = self.__s3OCREtree()  # get element s3xml
    self.s3ocrxml = etree.tostring(s3ocr_root, pretty_print=DEBUG)
    self.content = []

    s3ocr_layout_etree = self.layoutEtree
    # Define font size
    titlefontsize = 18
    sectionfontsize = 15
    regularfontsize = 13
    hintfontsize = 10

    # etree labels
    ITEXT = "label"
    HINT = "comment"
    TYPE = "type"
    HASOPTIONS = "has_options"
    LINES = "lines"
    BOXES = "boxes"
    REFERENCE = "reference"
    RESOURCE = "resource"

    # l10n
    l10n = {
        "datetime_hint": {
            "date": T("fill in order: day(2) month(2) year(4)"),
            "datetime": T("fill in order: hour(2) min(2) day(2) month(2) year(4)"),
        },
        "boolean": {
            "yes": T("Yes"),
            "no": T("No"),
        },
        "select": {
            "multiselect": T("Select one or more option(s) that apply"),
            "singleselect": T("Select any one option that apply"),
        },
    }

    # Print the etree
    for eachresource in s3ocr_root:
        # Create resource element of ocr layout xml
        s3ocr_layout_resource_etree =\
            etree.SubElement(s3ocr_layout_etree,
                             "resource", name=eachresource.attrib.get("name"))

        styleSheet = getStyleSheet()
        self.content.append(DrawHrLine(0.5))
        self.content.append(Paragraph(html_unescape_and_strip(eachresource.attrib.get(ITEXT,
                                                                                      eachresource.attrib.get("name"))),
                                      styleSheet["Section"]))
        self.content.append(DrawHrLine(0.5))

        for eachfield in eachresource.iterchildren():
            # Create field element of ocr layout xml
            s3ocr_layout_field_etree =\
                etree.SubElement(s3ocr_layout_resource_etree,
                                 "field",
                                 name=eachfield.attrib.get("name"),
                                 type=eachfield.attrib.get("type"))

            if eachfield.attrib.get(REFERENCE) == "1":
                s3ocr_layout_field_etree.set(REFERENCE,
                                             "1")
                s3ocr_layout_field_etree.set(RESOURCE,
                                             eachfield.attrib.get(RESOURCE))

            fieldlabel = eachfield.attrib.get(ITEXT)
            spacing = " " * 5
            fieldhint = self.__trim(eachfield.attrib.get(HINT))

            if fieldhint != "" and fieldhint != None:
                self.content.append(Paragraph(html_unescape_and_strip("%s%s( %s )" %
                                                                      (fieldlabel,
                                                                       spacing,
                                                                       fieldhint)),
                                              styleSheet["Question"]))

            else:
                self.content.append(Paragraph(html_unescape_and_strip(fieldlabel),
                                              styleSheet["Question"]))

            if eachfield.attrib.get("readable", "False") == "True" and \
                    eachfield.attrib.get("writable", "False") == "False":
                self.content.append(Paragraph(html_unescape_and_strip(eachfield.attrib.get("default",
                                                                                           "No default Value")),
                                              styleSheet["DefaultAnswer"]))

                # Remove the layout component of empty fields
                s3ocr_layout_resource_etree.remove(s3ocr_layout_field_etree)

            elif eachfield.attrib.get(HASOPTIONS) == "True":
                fieldtype = eachfield.attrib.get(TYPE)
                # if the field has to be shown with options
                if fieldtype == "boolean":
                    bool_text = l10n.get("boolean")
                    self.content.append(DrawOptionBox(bool_text.get("yes").
                                                      decode("utf-8"),
                                                      s3ocr_layout_field_etree,
                                                      "yes"))

                    self.content.append(DrawOptionBox(bool_text.get("no").
                                                      decode("utf-8"),
                                                      s3ocr_layout_field_etree,
                                                      "no"))

                else:
                    if fieldtype == "multiselect":
                        option_hint = l10n.get("select").get("multiselect")
                    else:
                        option_hint = l10n.get("select").get("singleselect")

                    s3ocrselect = eachfield.getchildren()[0]
                    numoptions = len(s3ocrselect.getchildren())

                    if numoptions <= MAX_FORM_OPTIONS_LIMIT:
                        s3ocr_layout_field_etree.attrib["limitcrossed"] = "1"
                        self.content.append(DrawHintBox(option_hint.
                                                        decode("utf-8")))

                        for eachoption in s3ocrselect.iterchildren():
                            self.content.append(DrawOptionBox(eachoption.text,
                                                              s3ocr_layout_field_etree,
                                                              eachoption.attrib.get("value")))
                    else:
                        self.content.append(DrawHintBox(
                            T("Enter a value carefully without spelling mistakes, this field will be crosschecked.").decode("utf-8")))
                        for eachtextbox in xrange(2):
                            self.content.append(StringInputBoxes(numBoxes=None,
                                                                 etreeElem=s3ocr_layout_field_etree))
            else:
                # It is a text field
                fieldtype = eachfield.attrib.get(TYPE)
                BOXES_TYPES = ["string", "textbox", "integer",
                               "double", "date", "datetime", ]
                if fieldtype in BOXES_TYPES:
                    if fieldtype in ["string", "textbox"]:
                        # form.linespace(3)
                        num_lines = int(eachfield.attrib.get("lines",
                                                             1))
                        for eachline in xrange(num_lines):
                            self.content.append(StringInputBoxes(numBoxes=None,
                                                                 etreeElem=s3ocr_layout_field_etree))

                    elif fieldtype in ["integer", "double"]:
                        num_boxes = int(eachfield.attrib.get("boxes",
                                                             9))
                        self.content.append(StringInputBoxes(numBoxes=num_boxes,
                                                             etreeElem=s3ocr_layout_field_etree))

                    elif fieldtype in ["date", "datetime"]:
                        # Print hint
                        hinttext = \
                            l10n.get("datetime_hint").get(
                                fieldtype).decode("utf-8")
                        self.content.append(DrawHintBox(hinttext))

                        if fieldtype == "datetime":
                            self.content.append(
                                DateTimeBoxes(s3ocr_layout_field_etree))
                        elif fieldtype == "date":
                            self.content.append(
                                DateBoxes(s3ocr_layout_field_etree))

                else:
                    self.r.error(501, self.manager.PARSE_ERROR)
                    print sys.stderr("%s :invalid field type: %s" %
                                     (eachfield.attrib.get("name"),
                                      fieldtype))
    return
