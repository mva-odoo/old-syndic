# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ActeDeBaseType(models.AbstractModel):
    _name = 'syndic.signalitic.base.type'
    _description = 'syndic.signalitic.base.type'

    name = fields.Char('Acte de base', required=True)


class ActeDeBase(models.AbstractModel):
    _name = 'syndic.signalitic.base'
    _description = 'syndic.signalitic.base'

    name = fields.Char('Description', required=True)
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    date = fields.Date('Date')
    note = fields.Char('Note')
    display_type = fields.Selection([
        ('line_note', 'line_note'),
        ('line_section', 'line_section')
    ])
    sequence = fields.Integer('Sequence')
