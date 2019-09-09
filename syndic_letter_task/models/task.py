from odoo import api, fields, models, _


class Task(models.Model):
    _inherit = 'syndic.claim'

    letter_ids = fields.One2many('letter.letter', 'task_id', 'Courrier')
    all_message_ids = fields.Many2many(
        'mail.message', string="All messages", 
        compute='_compute_all_message_ids', 
        )
    
    @api.depends('message_ids', 'letter_ids', 'letter_ids.message_ids')
    def _compute_all_message_ids(self):
        for task in self:
            task.all_message_ids = task.message_ids | task.letter_ids.mapped('message_ids')
    
    def open_letter(self):
        self.ensure_one()
        return {
            'name': _('Courrier'),
            'view_mode': 'form',
            'res_model': 'letter.letter',
            'type': 'ir.actions.act_window',
            'context': {'default_task_id': self.id}
        }
