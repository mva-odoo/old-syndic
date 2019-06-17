from odoo import api, fields, models


class Building(models.Model):
    _inherit = 'syndic.building'

    period = fields.Selection([
        ('mensuel', 'Mensuel'),
        ('trimestrielle', 'Trimestriel'),
    ], 'Période')

    accountant_id = fields.Many2one(
        'res.users',
        'Comptable',
        domain=[
            (
                'groups_id.name',
                'in',
                ['Syndic/Employe', 'Syndic/Manager']
            )
        ]
    )
