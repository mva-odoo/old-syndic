# -*- coding: utf-8 -*-
{
    'name': 'Syndic Base',
    'version': '2.0',
    'description': """
Core mechanisms for the syndic modules.
    """,
    'category': 'Syndic',
    'depends': ['base', 'mail', 'syndic_web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rule.xml',
        'views/settings.xml',
        'views/building.xml',
        'views/lot.xml',
        'views/partner.xml',
        'views/proprietaire.xml',
        'views/locataire.xml',
        'views/fournisseur.xml',
        'views/mutation.xml',
        'views/technical_field.xml',
        'views/res_config_setting_views.xml',
    ],
    'demo': [
        'demos/users.xml',
        'demos/city.xml',
        'demos/building.xml',
    ],
    'application': True,
}
