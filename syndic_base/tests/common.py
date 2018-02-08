# -*- coding: utf-8 -*-

from odoo.tests import common


class TestSyndicCommon(common.TransactionCase):

    def setUp(self):
        super(TestSyndicCommon, self).setUp()

        # Usefull models
        self.Users = self.env['res.users']
        self.Building = self.env['syndic.building']
        self.Lot = self.env['syndic.lot']

        # User groups
        self.serge = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_user_serge')
        self.sandrine= self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_user_sandrine')
        self.florence= self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_user_florence')

        # city
        self.wavre= self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_demo_city_wavre')

        # building
        self.gemini = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_demo_building_gemini')

        # owner
        self.sgimmo = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_partner_gemini_owner')

        # Lot
        self.A1 = self.env['ir.model.data'].xmlid_to_res_id('syndic_base.syndic_gemini_lot1')