from odoo import api, fields, models


class Claim(models.Model):
    _inherit = 'syndic.claim'

    name = fields.Char(string='Name')
