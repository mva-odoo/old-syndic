from odoo import api, fields, models, _


class Task(models.Model):
    _inherit = 'letter.letter'

    task_id = fields.Many2one('syndic.claim', 'Tâche')
