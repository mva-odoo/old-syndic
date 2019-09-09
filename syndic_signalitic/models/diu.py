# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PermisBaseType(models.Model):
    _name = 'diu.base.type'
    _inherit = 'syndic.signalitic.base'


class PermisBase(models.Model):
    _name = 'diu.base'
    _inherit = 'syndic.signalitic.base'

    type_id = fields.Many2one('diu.base.type', 'Type')
