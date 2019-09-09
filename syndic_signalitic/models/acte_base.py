# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ActeDeBaseType(models.Model):
    _name = 'acte.base.type'
    _inherit = 'syndic.signalitic.base'


class ActeDeBase(models.Model):
    _name = 'acte.base'
    _inherit = 'syndic.signalitic.base'

    type_id = fields.Many2one('acte.base.type', 'Type')
