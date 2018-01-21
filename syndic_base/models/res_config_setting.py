# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_syndic_sub_lot = fields.Boolean('Ajout des sous-lots')
    module_tech_fields = fields.Boolean('Création de fiche technique possible')
    module_pdf_viewer = fields.Boolean('Visionner le PDF avant de le downloader')
    module_syndic_letter = fields.Boolean('Ecrire du courrier papier')
