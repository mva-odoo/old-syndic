# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class SuiviFacture(models.TransientModel):
    _name = 'syndic.facturation.generation'
    _description = 'Generer des factures honoraire'

    trimestre = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Trimestre', required=True)
    year_id = fields.Many2one('syndic.honoraire.year', u'Année', required=True)
    date = fields.Date('Date', default=lambda *a: fields.date.today(), required=True)

    def invoice_generate(self):
        self.ensure_one()
        invoices = self.env['account.move']

        for immeuble in self.year_id.mapped('honoraire_ids.building_id'):
            frais = self.env['syndic.honoraire'].search([('year_id', '=', self.year_id.id), ('building_id', '=', immeuble.id)], limit=1)

            frais_admin_vals = {
                'date': self.date,
                'date_invoice': self.date,
                'trimestre': self.trimestre,
                'year': self.year_id.name,
                'name': 'Frais administratifs',
                'price_unit': frais.frais_admin,
                'quantity': 1,
                'account_id': self.env.ref('l10n_be.1_a7010').id,

            }

            honoraire_vals = {
                'trimestre': self.trimestre,
                'year': self.year_id.name,
                'name': 'Honoraires',
                'price_unit': frais.honoraire,
                'quantity': 1,
                'account_id': self.env.ref('l10n_be.1_a7010').id,

            }
            
            if immeuble.is_merge:
                invoices |= self.env['account.move'].create({
                    'date': self.date,
                    'date_invoice': self.date,
                    'partner_id': immeuble.company_id.partner_id.id,
                    'invoice_line_ids': [(0, 0, frais_admin_vals), (0, 0, honoraire_vals)]
                })

            else:
                invoices |= self.env['account.move'].create({
                    'date': self.date,
                    'date_invoice': self.date,
                    'partner_id': immeuble.company_id.partner_id.id,
                    'invoice_line_ids': [(0, 0, frais_admin_vals)]
                })

                invoices |= self.env['account.move'].create({
                    'date': self.date,
                    'date_invoice': self.date,
                    'partner_id': immeuble.company_id.partner_id.id,
                    'invoice_line_ids': [(0, 0, honoraire_vals)]
                })

        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [('id', 'in', invoices.ids)]
        return action
