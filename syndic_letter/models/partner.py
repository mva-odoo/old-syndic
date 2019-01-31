from odoo import models, fields, api, exceptions

from mako.template import Template


class PieceJointe(models.Model):
    _inherit = 'res.partner'

    def _get_mako_template(self, contenu, vals):
        mytemplate = Template(contenu)
        return mytemplate.render(**vals)
