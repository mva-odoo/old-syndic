# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Bank(models.Model):
    _inherit = 'res.partner.bank'

    @api.model
    def create(self, values):
        company_id = values.get('company_id')
        if company_id:
            values['partner_id'] = self.env['res.company'].browse(company_id).partner_id.id
        return super(Bank, self).create(values)
    
