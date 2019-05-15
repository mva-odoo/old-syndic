from odoo import api, fields, models, _


class Task(models.Model):
    _inherit = 'letter.letter'

    task_id = fields.Many2one('syndic.claim', 'Tâche')

    def print_letter(self):
        res = super(Task, self).print_letter()
        for letter in self:
            context = res.get('context')
            mails = context.get('mails')
            if mails:
                mails = mails[0]
            letter.task_id.message_post(body='%s' % mails.body_html)
        return res
