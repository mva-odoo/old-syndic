# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Immeuble(models.Model):
    _inherit = 'syndic.building'

    @api.model
    def _auto_init(self):
        buildings = self.search([('signalitic_id', '=', False)])
        for building in buildings:
            building.write({
                'signalitic_id': self.env['syndic.building.signalitic'].create({}).id
            })
        return super()._auto_init()

    signalitic_id = fields.Many2one(
        'syndic.building.signalitic',
        required=True, ondelete="cascade",
        delegate=True, string='Immeuble'
    )
