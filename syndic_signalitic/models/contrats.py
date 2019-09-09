# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ContratPrestationBaseType(models.Model):
    _name = 'contrat.prestations.base.type'
    _inherit = 'syndic.signalitic.base'


class ContratPrestationBase(models.Model):
    _name = 'contrat.prestations.base'
    _inherit = 'syndic.signalitic.base'

    type_id = fields.Many2one('contrat.prestations.base.type', 'Type')


class ContratfournituresBaseType(models.Model):
    _name = 'contrat.fournitures.base.type'
    _inherit = 'syndic.signalitic.base'


class ContratfournituresBase(models.Model):
    _name = 'contrat.fournitures.base'
    _inherit = 'syndic.signalitic.base'

    type_id = fields.Many2one('contrat.fournitures.base.type', 'Type')


class ContratrecettesBaseType(models.Model):
    _name = 'contrat.recettes.base.type'
    _inherit = 'syndic.signalitic.base'


class ContratrecettessBase(models.Model):
    _name = 'contrat.recettes.base'
    _inherit = 'syndic.signalitic.base'

    type_id = fields.Many2one('contrat.recettes.base.type', 'Type')
