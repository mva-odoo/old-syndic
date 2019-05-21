from odoo import api, fields, models


class Building(models.Model):
    _inherit = 'syndic.building'

    period = fields.Selection([
        ('mensuel', 'Mensuel'),
        ('trimestrielle', 'Trimestriel'),
    ])
    