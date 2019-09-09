# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class Country(models.Model):
    _inherit = 'res.country'
    _order = 'name asc'
