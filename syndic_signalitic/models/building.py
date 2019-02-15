# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Immeuble(models.Model):
    _inherit = 'syndic.building'

    signalitic_id = fields.Many2one(
        'syndic.building.signalitic',
        required=True, ondelete="cascade",
        delegate=True, string='Immeuble'
    )
