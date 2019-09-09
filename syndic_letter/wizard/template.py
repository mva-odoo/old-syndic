from odoo import models, api, fields


class TemplateMail(models.TransientModel):
    _name = 'syndic.template.mail'
    _description = 'syndic.template.mail'

    def _default_body(self):
        if self._context.get('active_id'):
            letter = self.env['letter.letter'].browse(self._context['active_id'])
            return letter.contenu

    name = fields.Char('name', required=True)
    body_html = fields.Html('Modèle', required=True, default=_default_body)

    def save_template(self):
        self.ensure_one()
        self.env['letter.model'].create({
            'name': self.name,
            'text': self.body_html,
        })
