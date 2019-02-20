# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Building(models.Model):
    _inherit = 'syndic.building'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.EUR'))
    honoraire = fields.Monetary('Honoraire', groups='syndic_base.syndic_manager', track_visibility='onchange')
    frais_admin = fields.Monetary('Frais Administratif', groups='syndic_base.syndic_manager', track_visibility='onchange')

    count_invoice = fields.Integer('N° de factures', compute='_get_count_invoice')

    def get_invoice(self):
        self.ensure_one()
        action = self.env.ref('account.action_invoice_tree1').read()[0]
        action['domain'] = [
            ('partner_id', '=', self.company_id.partner_id.id)
        ]
        return action

    def _get_count_invoice(self):
        for record in self:
            record.count_invoice = self.sudo().env['account.invoice'].search_count([
                ('partner_id', '=', record.company_id.partner_id.id)
            ])
