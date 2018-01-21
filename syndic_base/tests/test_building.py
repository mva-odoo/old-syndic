# -*- coding: utf-8 -*-

from odoo.addons.syndic_base.tests.common import TestSyndicCommon
from odoo.exceptions import ValidationError, UserError, AccessError


class TestEventFlow(TestSyndicCommon):

    def test_00_building(self):
        # creation
        vals = {
            'name': 'ADFL',
            'num': '46',
            'zip': 1300,
            'city_id': self.wavre,
            'street': 'Rue Edouard Olivier, 27',
        }

        with self.assertRaises(AccessError):
            self.Building.sudo(self.serge).create(vals)

        self.adfl = self.Building.sudo(self.sandrine).create(vals)
        self.aloys =self.Building.sudo(self.florence).create({
            'name': 'ALOYS',
            'num': '140',
            'zip': 1300,
            'city_id': self.wavre,
            'street': 'Boulevard du Souverain 338',
        })

        # write
        with self.assertRaises(AccessError):
            self.adfl.sudo(self.serge).toggle_active()
        self.adfl.sudo(self.sandrine).toggle_active()
        self.adfl.sudo(self.florence).toggle_active()

        # read
        with self.assertRaises(AccessError):
            self.aloys.sudo(self.serge).read([], [])

        self.aloys.sudo(self.sandrine).read([], [])
        self.adfl.sudo(self.florence).read([], [])

        #unlink
        with self.assertRaises(AccessError):
            self.aloys.sudo(self.serge).unlink()
            self.aloys.sudo(self.sandrine).unlink()
        self.adfl.sudo(self.florence).unlink()


    def test_01_lot(self):
        vals = {
            'name': 'A1',
            'building_id': self.gemini,
            'owner_ids': [(6, 0, [self.env['res.users'].browse(self.serge).partner_id.id])],
        }
        with self.assertRaises(AccessError):
            self.Lot.sudo(self.serge).create(vals)

        self.Lot.sudo(self.sandrine).create(vals)
        self.Lot.sudo(self.florence).create(vals)

        # recheck read on a building where I am the owner
        self.Building.browse(self.gemini).sudo(self.serge).read()