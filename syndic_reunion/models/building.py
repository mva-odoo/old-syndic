# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Immeuble(models.Model):
    _inherit = 'syndic.building'

    reunion_ids = fields.One2many('letter.reunion', 'immeuble_id', 'Réunion')
    last_date = fields.Date('Dernière Réunion', compute='_get_last_ag')

    def _get_last_ag(self):
        for building in self:
            last_date = self.env['calendar.event'].search([
                ('building_id', '=', building.id),
                ('is_ag', '=', True),
            ]).start_datetime
            if last_date:
                building.last_date = last_date.date()
