# -*- coding: utf-8 -*-

from odoo.addons.syndic_base.tests.common import TestSyndicCommon
from odoo.exceptions import ValidationError, UserError, AccessError
import datetime


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
            self.Building.with_user(self.serge).create(vals)

        self.adfl = self.Building.with_user(self.sandrine).create(vals)
        self.aloys = self.Building.with_user(self.florence).create({
            'name': 'ALOYS',
            'num': '140',
            'zip': 1300,
            'city_id': self.wavre,
            'street': 'Boulevard du Souverain 338',
        })

        # write TODO: remove toggle  active doesn t exist any more replace with write ???
        #with self.assertRaises(AccessError):
        #    self.adfl.with_user(self.serge).toggle_active()
        #self.adfl.with_user(self.sandrine).toggle_active()
        #self.adfl.with_user(self.florence).toggle_active()

        fields = [
            'name',
            # 'lot_ids',
            # 'quotity_ids',
        ]

        # read
        with self.assertRaises(AccessError):
            self.aloys.with_user(self.serge).read([], fields)
        # import ipdb; ipdb.set_trace()
        # self.aloys.with_user(self.sandrine).read([], fields)
        # self.adfl.with_user(self.florence).read([], fields)

        # unlink
        with self.assertRaises(AccessError):
            self.aloys.with_user(self.serge).unlink()
            self.aloys.with_user(self.sandrine).unlink()
        self.adfl.with_user(self.florence).unlink()

    def test_01_lot(self):
        vals = {
            'name': 'A1',
            'building_id': self.gemini,
            'owner_id': self.env['res.users'].browse(self.serge).partner_id.id,
        }
        with self.assertRaises(AccessError):
            self.Lot.with_user(self.serge).create(vals)

        self.Lot.with_user(self.sandrine).create(vals)
        self.Lot.with_user(self.florence).create(vals)

        # recheck read on a building where I am the owner (we don't have access to the signalitic field)
        self.Building.browse(self.gemini).with_user(self.serge).read(['name', 'num'])

    def test_02_mutation(self):
        mutation = self.env['syndic.mutation'].create({
            'mutation_date': datetime.datetime.now(),
            'old_owner_ids': [(4, self.sgimmo)],
            'new_owner_id': self.env['res.partner'].create({'name': 'New Owner'}).id,
            'lot_ids': [(4, self.A1)],
        })
        mutation.mutation()

        self.assertIn('New Owner', self.env['syndic.lot'].browse(self.A1).owner_id.name)
        sgimmo = self.env['res.partner'].browse(self.sgimmo)
        print('---', sgimmo.name)
        self.assertTrue(sgimmo.is_old)
        self.assertFalse(sgimmo.is_proprietaire)
