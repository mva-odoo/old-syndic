from odoo import api, fields, models, _


class Task(models.Model):
    _inherit = 'syndic.claim'

    letter_ids = fields.One2many('letter.letter', 'task_id', 'Courrier')
    
    def open_letter(self):
        self.ensure_one()
        return {
            'name': _('Courrier'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'letter.letter',
            # 'view_id': False,
            'type': 'ir.actions.act_window',
            'context': {'default_task_id': self.id}
        }
