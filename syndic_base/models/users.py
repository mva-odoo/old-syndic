# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, SUPERUSER_ID


class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        if self.env.context.get('nocreate_user'):
            return self.env['res.users']
        return super(Users, self).create(vals)
