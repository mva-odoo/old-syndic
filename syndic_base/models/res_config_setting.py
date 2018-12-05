# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_syndic_sub_lot = fields.Boolean('Ajout des sous-lots')
    module_syndic_tech_fields = fields.Boolean('Fiche technique')
    module_pdf_viewer = fields.Boolean('Visionner le PDF avant de le downloader')
    module_syndic_letter = fields.Boolean('Ecrire lettre en format papier')
    module_syndic_avis = fields.Boolean('Ecrire Avis')
    module_syndic_reunion = fields.Boolean('Assemblée générale')
    module_syndic_gestion_privative = fields.Boolean('Gérer les gestion privative')
    module_syndic_documents = fields.Boolean('Partager des documents')
    module_syndic_caim = fields.Boolean('Gerer les sinistres')
