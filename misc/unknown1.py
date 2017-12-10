def evenement_est(response, lettre_commande):
    # Our container for 'Flowable' objects
    elements = []

    # Main TableFontsize
    petitePolice = 10
    basePolice = 12
    grandePolice = 14

    fontsize_style = ('FONTSIZE', (0, 0), (-1, -1), basePolice)

    rootPath = '/var/www/vhosts/backupmix.com/httpdocs/greta/administration/pdf/img/'
    # Empty checkbox
    empty_checkbox = Image(
        rootPath + "checkbox_empty.jpg", width=18, height=18)

    # Checked checkbox
    checked_checkbox = Image(
        rootPath + "checkbox_checked.jpg", width=18, height=18)

    checks_box = (empty_checkbox, checked_checkbox)

    # A basic document for us to write to 'rl_hello_platypus.pdf'
    #doc = SimpleDocTemplate("fiche_evenemment.pdf", rightMargin=10, leftMargin=10, topMargin=0, bottomMargin=5)
    doc = SimpleDocTemplate(response, rightMargin=10,
                            leftMargin=10, topMargin=0, bottomMargin=5)

    # Image en-tête
    evenementEst_Image = Image(
        rootPath + "evenement_est.jpg", width=573, height=159)
    evenementEst_Image.spaceAfter = 30
    elements.append(evenementEst_Image)

    # Create two 'Paragraph' Flowables and add them to our 'elements'
    #elements.append(Paragraph("The Platypus", styles['Heading1']))
    elements.append(Paragraph("<u>Type de prestation</u>",
                              styles.getSampleStyleSheet()['Heading2']))

    # Tableau type de prestations
    typePresta_data = [[empty_checkbox, 'BCA', checked_checkbox, 'CIBLE', empty_checkbox, 'OP CREA',
                        empty_checkbox, 'ECCP', empty_checkbox, 'MOB', empty_checkbox, 'STR', empty_checkbox, 'EPCE']]
    colonnesWidths = (20,            55,    20,             65,       20,            80,
                      20,             55,     20,           55,      20,         50,    20,          50)
    typePresta_style = TableStyle([fontsize_style,
                                   ('VALIGN', (1, 0), (1, 0), 'MIDDLE'),
                                   ('VALIGN', (3, 0), (3, 0), 'MIDDLE'),
                                   ('VALIGN', (5, 0), (5, 0), 'MIDDLE'),
                                   ('VALIGN', (7, 0), (7, 0), 'MIDDLE'),
                                   ('VALIGN', (9, 0), (9, 0), 'MIDDLE'),
                                   ('VALIGN', (11, 0), (11, 0), 'MIDDLE'),
                                   ('VALIGN', (13, 0), (13, 0), 'MIDDLE'),
                                   ])
    typePresta_style.spaceAfter = 10
    typePresta_table = Table(data=typePresta_data,
                             colWidths=colonnesWidths, style=typePresta_style)
    elements.append(typePresta_table)

    location_style = styles.getSampleStyleSheet()['Normal']
    location_style.spaceAfter = 10
    location_style.alignment = enums.TA_LEFT

    elements.append(Paragraph(u"<font size='12'><b>Nom du prestataire: </b>%s</font>" %
                              (lettre_commande.site.prestataire.nom,), location_style))
    elements.append(Paragraph(u"<font size='12'><b>Lieu de réalisation: </b>%s</font>" %
                              (lettre_commande.site.nom,), location_style))
    elements.append(Paragraph(
        u"<font size='12'><b>Agence d'inscription: </b>%s</font>", location_style))

    tableData = [[u"Nom-Prénom du DE:", lettre_commande.nom + " " + lettre_commande.prenom, "", "", u"N° Identifiant:", lettre_commande.polemploi_id],
                 ["Date du premier RDV:", lettre_commande.ouverture_rdv.dateheure.date().strftime(
                     "%d/%m/%Y"), "", "", "Heure du RDV:", lettre_commande.ouverture_rdv.dateheure.time().strftime("%H:%M")],
                 ]
    tableStyle = TableStyle([fontsize_style,
                             #('ALIGN', (0,0), (5,0), 'RIGHT'),
                             ('FONT', (0, 0), (0, 1), 'Times-Bold'),
                             ('FONT', (4, 0), (4, 1), 'Times-Bold'),
                             ('ALIGN', (0, 0), (-1, -1), 'LEFT'),

                             ])
    table = Table(tableData, style=tableStyle)
    table.hAlign = 0
    #table.leftPadding = 0
    table.spaceAfter = 20
    elements.append(table)

    # Escpace
    #space1 = Spacer(width=450, height=20)
    # elements.append(space1)

    # Barre Horizontale
    barreHorizontale = Image(
        rootPath + "barre_horizontale.jpg", width=520, height=6)
    barreHorizontale.spaceAfter = 20
    elements.append(barreHorizontale)

    # Tableaux Premier RDV

    # DEMARRAGE DE PRESTATION

    demarragePresta_data = [[eval(get_image_ouverture_rdv(
        lettre_commande.ouverture_rdv, ouvertureRdv.PRESENT_C)), "A DEMARRE LA PRESTATION"], ]
    demarragePresta_style = TableStyle([('FONTSIZE', (1, 0), (1, 0), grandePolice),
                                        ('LEADING', (1, 0), (1, 0), 3),
                                        ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                        ])
    demarragePresta = Table(demarragePresta_data, style=demarragePresta_style)
    demarragePresta.hAlign = 0
    demarragePresta.spaceAfter = 10
    elements.append(demarragePresta)

    # REFUS PRESTATION
    refusPresta_data = [[eval(get_image_ouverture_rdv(lettre_commande.ouverture_rdv, ouvertureRdv.PRESENT_NC)), "N'A PAS ADHERE A LA PRESTATION"],
                        [None, "Indiquer le motif: " +
                            get_comments_ouverture_rdv(lettre_commande.ouverture_rdv)],
                        ]
    refusPresta_style = TableStyle([('FONTSIZE', (1, 0), (1, 0), grandePolice),
                                    ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                    ('FONTSIZE', (1, 1), (1, 1), petitePolice),
                                    ])
    refusPresta = Table(refusPresta_data, style=refusPresta_style)
    refusPresta.hAlign = 0
    refusPresta.spaceAfter = 10
    elements.append(refusPresta)

    # ABSENT
    absentPresta_data = [[eval(get_image_ouverture_rdv(lettre_commande.ouverture_rdv, ouvertureRdv.ABSENT)), "NE S'EST PAS PRESENTE"],
                         ]
    absentPresta_style = TableStyle([('FONTSIZE', (1, 0), (1, 0), grandePolice),
                                     ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                     ])
    absentPresta = Table(absentPresta_data, style=absentPresta_style)
    absentPresta.hAlign = 0
    absentPresta.spaceAfter = 10
    elements.append(absentPresta)

    # REPORT
    reportPresta_data = [[eval(get_image_ouverture_rdv(lettre_commande.ouverture_rdv, ouvertureRdv.REPORT)), "A DEMANDE AU PRESTATAIRE UN REPORT DU PREMIER RDV"],
                         [None,  "(8 jours maxi)"],
                         ]
    reportPresta_style = TableStyle([('FONTSIZE', (1, 0), (1, 0), grandePolice),
                                     ('FONTSIZE', (1, 1), (1, 1), basePolice),
                                     ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                     ])
    reportPresta = Table(reportPresta_data, style=reportPresta_style)
    reportPresta.hAlign = 0
    reportPresta.spaceAfter = 10
    elements.append(reportPresta)

    newDateTime_data = [[None, "Date du nouveau RDV: " + get_newdate_ouverture_rdv(lettre_commande.ouverture_rdv), "Heure du nouveau RDV: " + get_newtime_ouverture_rdv(lettre_commande.ouverture_rdv)],
                        ]
    newDateTime_style = TableStyle([('FONTSIZE', (0, 0), (-1, -1), basePolice),
                                    ])
    newDateTime = Table(newDateTime_data, style=newDateTime_style)
    newDateTime.hAlign = 0
    newDateTime.spaceAfter = 20
    elements.append(newDateTime)

    # Barre Horizontale
    elements.append(barreHorizontale)

    # ABANDON PRESTATION
    abandonPresta_data = [[empty_checkbox, "A ABANDONNE EN COURS DE PRESTATION A LA DATE DU:"],
                          [None, "Indiquer le motif:"]
                          ]
    abandonPresta_style = TableStyle([('FONTSIZE', (1, 0), (1, 0), grandePolice),
                                      ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                      ('FONTSIZE', (1, 1), (1, 1), basePolice),
                                      ])
    abandonPresta = Table(abandonPresta_data, style=abandonPresta_style)
    abandonPresta.hAlign = 0
    abandonPresta.spaceAfter = 20
    elements.append(abandonPresta)

    # Barre Horizontale
    elements.append(barreHorizontale)

    # DISCLAIMER
    disclaimer_style = styles.getSampleStyleSheet()['Normal']
    disclaimer_style.textColor = colors.grey
    disclaimer_style.fontSize = grandePolice
    disclaimer_style.alignment = enums.TA_CENTER
    disclaimer = Paragraph(
        "<strong>LES EVENEMENTS DOIVENT ETRE SIGNALES A LA PLATEFORME DES QUE POSSIBLE ET AU PLUS TARD DANS LES 48 HEURES -  01 49 44 42 86<strong>", disclaimer_style)
    elements.append(disclaimer)

    # Write the document to disk
    doc.build(elements)
