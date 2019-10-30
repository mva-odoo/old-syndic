# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Lot(models.Model):
    _name = 'syndic.lot'
    _description = 'Lots'
    _inherit = ['mail.thread']
    _order = 'building_id asc,name'

    name = fields.Char('Nom du lot', required=True)
    building_id = fields.Many2one('syndic.building', 'Immeuble')

    owner_id = fields.Many2one(
        'res.partner',
        'Propriétaire',
    )

    loaner_ids = fields.Many2many(
        'res.partner',
        'lot_locataire',
        string='Locataires',
    )
    type_id = fields.Many2one('syndic.type_lot', 'Type de lot')
    display_type = fields.Selection([
        ('line_section', 'Section'),
    ], string='Display')
    sequence = fields.Integer(string='Sequence')
    quotity_ids = fields.Many2many('syndic.quotite', string='Quotitées')
    quotity_line_ids = fields.One2many(
        'syndic.quotite.line',
        'lot_id',
        'Ligne de Quotitée'
    )
    quotity = fields.Integer('Quotitée')

    @api.model
    def create(self, vals):
        res = super(Lot, self).create(vals)
        quotities = res.building_id.quotity_ids.filtered(
            lambda s: s.type_id == s.env.ref('syndic_base.syndic_quotite_base')
        )
        for quotity in quotities:
            quotity._onchange_quotity()
        return res


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
        lot_ids = self.building_id.lot_ids.filtered(lambda s: s.display_type == False)
        lots = self.env['syndic.lot'].browse(lot_ids.ids)
        for lot in lots:
            values.append([
                0, 0,
                {
                    'lot_id': lot.id,
                    'lot_owner_id': lot.owner_id.id,
                    'value': lot.quotity
                }
            ])
        self.line_ids = values

    def reload_quotity(self):
        self.ensure_one()
        self._onchange_quotity()


class QuotityLine(models.Model):
    _name = 'syndic.quotite.line'
    _description = 'Quotity Line'
    _rec_name = 'lot_id'

    quotity_id = fields.Many2one('syndic.quotite', 'Quotitée')
    value = fields.Float('valeur')
    lot_id = fields.Many2one('syndic.lot', 'Lot')
    lot_name = fields.Char('Nom du Lot', related="lot_id.name")
    lot_owner_id = fields.Many2one('res.partner', string='Propriétaire')

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        self.lot_owner_id = self.lot_id.owner_id

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
