# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PlanDeBaseType(models.Model):
    _name = 'plan.base.type'
    _inherit = 'syndic.signalitic.base'


class PlanDeBase(models.Model):
    _name = 'plan.base'
    _inherit = 'syndic.signalitic.base'

    type_id = fields.Many2one('plan.base.type', 'Type')
