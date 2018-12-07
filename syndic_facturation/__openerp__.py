{
    'name': 'Facturation syndic',
    'version': '1.0',
    'category': 'Syndic',
    'description': """
    Facturation pour syndic
""",
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
    'depends': ['syndic_base'],
    'data': [
        'views/facturation.xml',
        'report/facture.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'datas/sequence.xml',
        'wizards/generate_invoice.xml',
    ],
    'installable': True,
}