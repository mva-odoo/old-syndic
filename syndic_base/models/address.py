# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class City(models.Model):
    _name = 'res.partner.city'
    _order = 'name'

    name = fields.Char('Ville', required=True)
    zip = fields.Char('Code Postal')
    country_id = fields.Many2one('res.country', 'Country')
    active = fields.Boolean('Actif', default=True)

class Country(models.Model):
    _inherit = 'res.country'
    _order = 'name asc'
