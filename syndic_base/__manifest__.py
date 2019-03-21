# -*- coding: utf-8 -*-
{
    'name': 'Syndic Base',
    'version': '2.0',
    'description': """
Core mechanisms for the syndic modules.
    """,
    'category': 'Syndic',
    'depends': [
        'base',
        'base_address_city',
        'mail',
        'web',
    ],
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
        'views/res_config_setting_views.xml',
        'views/users.xml',
        'views/backend.xml',
        'datas/res.city.csv',
        'datas/company.xml',
        'datas/lot_type.xml',
        'datas/quotite_type.xml',
        'report/immeuble.xml',
    ],
    'demo': [
        'demos/users.xml',
        'demos/building.xml',
    ],
    'application': True,
}
