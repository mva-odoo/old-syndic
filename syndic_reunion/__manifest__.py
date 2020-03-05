# -*- coding: utf-8 -*-
{
    'name': 'Syndic conseil de copropriete',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    Syndic conseil de copropriete
    """,
    'author': 'SGImmo SPRL',
    'depends': ['syndic_letter'],
    'website': 'https://sgimmo.be',
    'data': [
            'views/reunion.xml',
            'views/building.xml',
            'views/client_action.xml',
            'report/reunion.xml',
            'security/ir.model.access.csv',
        ],
    'qweb': [
        'static/src/xml/template.xml',
    ]
}
