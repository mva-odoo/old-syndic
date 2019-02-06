# -*- coding: utf-8 -*-

{
    'name': 'Syndic Letter',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    Syndic Lettre
    """,
    'author': 'SGImmo SPRL',
    'depends': ['syndic_base', 'mail', 'syndic_tools'],
    'website': 'https://sgimmo.be',
    'data': [
        'views/letter.xml',
        'wizard/template_mail.xml',
        'report/layout.xml',
        'report/letter.xml',
        'security/ir.model.access.csv',
    ],
}
