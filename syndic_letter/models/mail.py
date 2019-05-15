# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MailMail(models.Model):
    _inherit = 'mail.mail'

    letter_id = fields.Many2one('letter.letter', 'Lettre')
