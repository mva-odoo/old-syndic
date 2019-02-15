# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SignalitiqueImmeuble(models.Model):
    _name = 'syndic.building.signalitic'

    building_ids = fields.One2many('syndic.building', 'signalitic_id',
                                   string='Immeubles')
