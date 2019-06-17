# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Lot(models.Model):
    _name = 'syndic.lot'
    _description = 'Lots'
    _inherit = ['mail.thread']
    _order = 'building_id asc,name'

    name = fields.Char('Nom du lot', required=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    is_undivision = fields.Boolean('Indivision')
    owner_id = fields.Many2one(
        'res.partner',
        'Propriétaire',
        domain=[
            '|',
            '|',
            ('is_proprietaire', '=', True),
            ('is_locataire', '=', True),
            '|',
            ('is_old', '=', True),
            ('supplier', '=', True),
        ]
    )
    owner_ids = fields.Many2many(
        'res.partner',
        'lot_proprietaire',
        string='Propriétaires',
        domain=[
            '|',
            '|',
            ('is_proprietaire', '=', True),
            ('is_locataire', '=', True),
            '|',
            ('is_old', '=', True),
            ('supplier', '=', True),
        ]
    )
    loaner_ids = fields.Many2many(
        'res.partner',
        'lot_locataire',
        string='Locataires',
        domain=[
            '|',
            '|',
            ('is_proprietaire', '=', True),
            ('is_locataire', '=', True),
            '|',
            ('is_old', '=', True),
            ('supplier', '=', True),
        ])
    type_id = fields.Many2one('syndic.type_lot', 'Type de lot')
    display_type = fields.Selection([
        ('line_section', 'line_section'),
        ('line_section', 'line_section'),
    ], string='Display')
    sequence = fields.Integer(string='Sequence')
    quotity_ids = fields.Many2many('syndic.quotite', string='Quotitée')
    quotity_line_ids = fields.One2many(
        'syndic.quotite.line',
        'lot_id',
        'Ligne de Quotitée'
    )
    quotity = fields.Integer('Quotitée')

    @api.onchange('is_undivision')
    def onchangeundivision(self):
        if self.is_undivision:
            if not self.owner_ids:
                domain = []
            else:
                domain = [('id', 'in', self.owner_ids.ids)]

            return {
                'domain': {
                    'owner_id': domain,
                }
            }

    @api.onchange('owner_id')
    def onchange_owner(self):
        self.owner_ids = self.owner_id

    @api.onchange('owner_ids')
    def onchange_owners(self):
        if self.owner_id not in self.owner_ids:
            self.owner_id = self.env['res.partner']


class TypeLot(models.Model):
    _name = 'syndic.type_lot'
    _description = 'Type de lot'
    _order = 'name'

    name = fields.Char('Type de lot', required=True)


class Quotitee(models.Model):
    _name = 'syndic.quotite'
    _description = 'Quotitée'
    _rec_name = 'type_id'

    type_id = fields.Many2one('syndic.quotite.type', 'Quotitée', required=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    line_ids = fields.One2many(
        'syndic.quotite.line',
        'quotity_id',
        'Quotitées'
    )

    @api.onchange('type_id')
    def _onchange_quotity(self):
        values = [(6, 0, [])]
        for lot in self.building_id.lot_ids.filtered(lambda s: s.display_type == False):
            values.append([
                0,
                0,
                {
                    'lot_id': lot.id,
                    'lot_owner_ids': [
                        (6, 0, lot.owner_ids.ids),
                    ],
                    'value': lot.quotity
                }
            ])
        self.line_ids = values


class QuotityLine(models.Model):
    _name = 'syndic.quotite.line'
    _description = 'Quotity Line'
    _rec_name = 'lot_id'

    quotity_id = fields.Many2one('syndic.quotite', 'Quotitée')
    value = fields.Float('valeur')
    lot_id = fields.Many2one('syndic.lot', 'Lot')
    lot_name = fields.Char('Nom du Lot', related="lot_id.name")
    lot_owner_ids = fields.Many2many('res.partner', string='Propriétaire')

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        self.lot_owner_ids = self.lot_id.owner_ids

    @api.multi
    def write(self, values):
        for quotity_line in self:
            if values.get('value'):
                quotity_line.lot_id.write({
                    'quotity': values['value'],
                })

        return super(QuotityLine, self).write(values)


class Quotitee_type(models.Model):
    _name = 'syndic.quotite.type'
    _description = 'syndic.quotite.type'

    name = fields.Char(string='Name', required=True)
