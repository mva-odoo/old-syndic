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

    def open_mutation(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.wizard_action_mutation').read()[0]
        action['context'] = {
            'default_old_owner_ids': self.owner_ids.ids,
            'default_lot_ids': self.ids,
        }
        return action


class TypeLot(models.Model):
    _name = 'syndic.type_lot'
    _description = 'Type de lot'
    _order = 'name'

    name = fields.Char('Type de lot', required=True)
