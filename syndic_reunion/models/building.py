# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Immeuble(models.Model):
    _inherit = 'syndic.building'

    reunion_ids = fields.One2many('letter.reunion', 'immeuble_id', 'Réunion')

