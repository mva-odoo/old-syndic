# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TechBuilding(models.Model):
    _inherit = 'syndic.building'

    fiche_signalitic_ids = fields.One2many('building.signalitic',
                                           'building_id',
                                           string='Fiche Signalitique',
                                           readonly=True)  # One2many but it is a relation o2o

    sign_mois_rel = fields.Selection(string='Mois', related='fiche_signalitic_ids.date_mois')
    sign_quizaine_rel = fields.Selection(string='Quinzaine', related='fiche_signalitic_ids.date_quizaine')
