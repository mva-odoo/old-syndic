# -*- coding: utf-8 -*-

from odoo import api, fields, models


class GestionPrivative(models.Model):
    _name = 'syndic.gestion.privative'

    name = fields.Char(string="Gestion Privative")
    partner_id = fields.Many2one('res.partner', 'Propriétaire')
    num = fields.Integer('Numero')
    bank_account_id = fields.Many2one('res.partner.bank', 'Compte en Banque')
    test_lot_ids = fields.One2many('syndic.gestion.privative.lot', 'gestion_id', 'Lots')
    lot_ids = fields.One2many('syndic.lot', 'gestion_id', 'Lots')


class GestionPrivativeLotOLD(models.Model):
    _name = 'syndic.gestion.privative.lot'

    name = fields.Char('Lot')
    building_id = fields.Many2one('syndic.gestion.privative.building', 'Immeuble')
    gestion_id = fields.Many2one('syndic.gestion.privative', 'Gestion Privative')


class GestionPrivativeLot(models.Model):
    _inherit = 'syndic.lot'

    gestion_id = fields.Many2one('syndic.gestion.privative', 'Gestion Privative')


class GestionPrivativeBuilding(models.Model):
    _name = 'syndic.gestion.privative.building'

    name = fields.Char('Immeuble')
