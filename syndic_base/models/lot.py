# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Lot(models.Model):
    _name = 'syndic.lot'
    _description = 'Lots'
    _inherit = ['mail.thread']
    _order = 'building_id asc,name'

    name = fields.Char('Nom du lot', required=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    owner_ids = fields.Many2many('res.partner', 'lot_proprietaire', string='Propriétaires')
    loaner_ids = fields.Many2many('res.partner', 'lot_locataire', string='Locataires')
    quotities = fields.Float('Quotitées')
    type_id = fields.Many2one('syndic.type_lot', 'Type de lot')


class TypeLot(models.Model):
    _name = 'syndic.type_lot'
    _order = 'name'

    name = fields.Char('Type de lot', required=True)
