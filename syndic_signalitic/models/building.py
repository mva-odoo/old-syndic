# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Immeuble(models.Model):
    _inherit = 'syndic.building'

    acte_de_base_ids = fields.One2many('acte.base',
                                       'immeuble_id', string='actes de base')
    permis_ids = fields.One2many('permis.base',
                                 'immeuble_id', string='Permis')
    plan_ids = fields.One2many('plan.base',
                               'immeuble_id', string='Plan')
    contrat_prestation_ids = fields.One2many('contrat.prestations.base',
                                             'immeuble_id',
                                             string='Contrats prestations')
    contrat_fournitures_ids = fields.One2many('contrat.fournitures.base',
                                              'immeuble_id',
                                              string='Contrats fournitures')
    contrat_recettes_ids = fields.One2many('contrat.fournitures.base',
                                           'immeuble_id',
                                           string='Contrats recettes')
