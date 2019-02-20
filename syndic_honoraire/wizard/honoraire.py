# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions


class SuiviFacture(models.TransientModel):
    _name = 'syndic.facturation.generation'
    _description = 'Generer des factures honoraire'

    def _get_immeuble(self):
        return self._context.get('active_ids', []) or []

    all_building = fields.Boolean('Tout les immeubles', default=True)
    index = fields.Float('Index')
    immeuble_ids = fields.Many2many('syndic.building', string='Immeubles', default=_get_immeuble)
    trimestre = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Trimestre', required=True)
    year = fields.Char(u'Année', required=True)
    date = fields.Date('Date', default=lambda *a: fields.date.today(), required=True)

    is_merge = fields.Boolean('Fusionner les frais administratifs avec les honoraires')

    @api.multi
    def invoice_generate(self):
        self.ensure_one()
        invoices = self.env['account.invoice']
        main_company = self.env.ref('base.main_company')
        # Change company to avoid issue with multi company due to the building
        old_company = self.env.user.company_id
        self.env.user.write({'company_id': main_company.id})

        vals = {
           'date': self.date,
           'trimestre': self.trimestre,
           'year': self.year,
        }

        immeubles = self.immeuble_ids if self.immeuble_ids else self.env['syndic.building'].search([])

        for immeuble in immeubles:
            vals['partner_id'] = immeuble.company_id.partner_id.id
            h_vals = vals.copy()
            honoraire = immeuble.honoraire * (1 + (self.index)/100) if self.index else immeuble.honoraire
            h_vals['invoice_line_ids'] = lines = [
               (0, 0, {
                   'name': 'Honoraires',
                   'price_unit': honoraire,
                   'quantity': 1,
                   'account_id': self.env.ref('l10n_be.1_a7010').id,
               })
            ]

            fraisadmin = immeuble.frais_admin * (1 + (self.index/100)) if self.index else immeuble.frais_admin
            if not self.is_merge:
                lines = []
                invoices |= self.env['account.invoice'].create(h_vals)

            lines.append(
               (0, 0, {
                   'name': 'Frais administratifs',
                   'price_unit': fraisadmin,
                   'quantity': 1,
                   'account_id': self.env.ref('l10n_be.1_a7010').id,
               })
            )
            vals['invoice_line_ids'] = lines

            invoices |= self.env['account.invoice'].create(vals)

            immeuble.write({
                'frais_admin': fraisadmin,
                'honoraire': honoraire,
            })
            self.env.user.write({'company_id': old_company.id})

        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['domain'] = [
            ('id', 'in', invoices.ids)
        ]
        return action
