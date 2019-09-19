# -*- coding: utf-8 -*-
{
    'name': 'Syndic calendar',
    'version': '0.1',
    "category": 'Syndic',
    'description': """
    calendar
    """,
    'author': 'OpenERP SA',
    'depends': ['calendar', 'syndic_base'],
    'website': 'http://www.openerp.com',
    'data': [
        'views/calendar.xml',
        'views/backend.xml',
        'views/res_config.xml',
        # 'security/ir.model.access.csv',
        ],
}
