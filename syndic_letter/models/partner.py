from odoo import models, fields, api, exceptions

from mako.template import Template
from jinja2 import Template


class PieceJointe(models.Model):
    _inherit = 'res.partner'

    def _get_jinja_template(self, contenu, vals):
        t = Template(contenu)
        return t.render(**vals)
