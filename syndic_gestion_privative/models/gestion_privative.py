# -*- coding: utf-8 -*-

from odoo import api, fields, models


class GestionPrivativeLot(models.Model):
    _inherit = 'syndic.lot'

    gestion_id = fields.Many2one('syndic.gestion.privative', 'Gestion Privative')


class GestionPrivative(models.Model):
    _name = 'syndic.gestion.privative'
    _description = 'syndic.gestion.privative'

    name = fields.Char(string="Gestion Privative", required=True)
    partner_id = fields.Many2one('res.partner', 'Propriétaire', required=True)
    num = fields.Integer('Numero')
    bank_account_id = fields.Many2one('res.partner.bank', 'Compte en Banque')
    lot_ids = fields.One2many('syndic.lot', 'gestion_id', 'Lots')
