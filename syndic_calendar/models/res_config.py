from odoo import models, fields, api, exceptions


class Company(models.Model):
    _inherit = 'res.company'

    month_delay = fields.Integer('Delais pour AG', default="3")


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    month_delay = fields.Integer('Delais pour AG', related="company_id.month_delay", readonly=False)
