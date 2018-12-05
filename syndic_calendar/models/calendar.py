# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions


class CreateLetter(models.Model):
    _inherit = 'calendar.event'

    building_id = fields.Many2one('syndic.building', string='Immeuble')
    attendee_string = fields.Char('Participants', compute='compute_participant')

    @api.one
    def compute_participant(self):
        self.attendee_string = ','.join(self.attendee_ids.mapped('name'))
