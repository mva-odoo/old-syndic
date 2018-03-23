# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SubLot(models.Model):
    _inherit = 'syndic.lot'

    parent_id = fields.Many2one('syndic.lot', string='Lot')
    child_ids = fields.One2many('syndic.lot', 'parent_id', string='sous-lots')
