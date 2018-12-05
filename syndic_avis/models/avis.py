# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
# from openerp.addons.syndic_tools.syndic_tools import SyndicTools


class LetterAvis(models.Model):
    _name = 'letter.avis'
    _order = 'create_date desc'

    name = fields.Char(u'Nom de l’avis', required=True)
    text = fields.Html('Texte')
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble')
    create_date = fields.Datetime(u'Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    date = fields.Date(u'Date de création', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)
    type_id = fields.Many2one('type.avis', "Type d'avis", required=True)
    avis_model_id = fields.Many2one("letter.avis.model", "Modele d'avis")

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = SyndicTools().french_date(self.date)

    @api.onchange('avis_model_id')
    def onchange_letter_avis_model(self):
        self.text = self.avis_model_id.text


class TypeAvis(models.Model):
    _name = 'type.avis'

    name = fields.Char('Type', required=True)
