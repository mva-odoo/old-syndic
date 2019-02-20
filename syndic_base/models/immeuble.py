# -*- coding: utf-8 -*-

from odoo import api, fields, models

_MONTH = [
    (1, 'Janvier'),
    (2, 'Fevrier'),
    (3, 'Mars'),
    (4, 'Avril'),
    (5, 'Mai'),
    (6, 'Juin'),
    (7, 'Juillet'),
    (8, 'Aout'),
    (9, 'Septembre'),
    (10, 'Octobre'),
    (11, 'Novembre'),
    (12, 'Decembre')
]


class Immeuble(models.Model):
    _name = 'syndic.building'
    _inherit = ['mail.thread']
    _description = 'Immeubles'
    _order = 'name asc'

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, ondelete="cascade", delegate=True)

    city_id = fields.Many2one('res.city', 'Ville')

    BCE = fields.Char('BCE')
    num = fields.Integer(u"N°", required=True)
    zip = fields.Char(default='')
    total_quotites = fields.Float(compute='_get_quotity', string='Total des Quotitées')

    lot_ids = fields.One2many('syndic.lot', 'building_id', 'Lots')
    lot_count = fields.Integer(compute='_get_quotity', string='Nombre de lots')

    owner_count = fields.Integer(compute='_get_quotity', string='Nombre de Propriétaires')
    loaner_count = fields.Integer(compute='_get_quotity', string='Nombre de Locataires')

    note = fields.Text('Notes')

    manager_id = fields.Many2one('res.users', 'Manager',
                                 domain="[('groups_id.name','in',['Syndic/Employe','Syndic/Manager'])]")

    is_lock = fields.Boolean('Bloquer')

    is_building = fields.Boolean('Est un immeuble', default=True)

    date_mois = fields.Selection(_MONTH, 'Mois')
    date_quizaine = fields.Selection([('1', '1'), ('2', '2')], 'Quinzaine')

    supplier_ids = fields.One2many('res.partner.contractual',
                                   'building_id',
                                   'Corps de métier')

    @api.model
    def _auto_init(self):
        self.env.ref('base.res_company_rule_employee').write({'active': False})
        res = super(Immeuble, self)._auto_init()

    @api.model
    def create(self, vals):
        vals['is_lock'] = True
        return super(Immeuble, self).create(vals)

    @api.onchange('zip')
    def _onchange_zip(self):
        return {
            'domain': {'city_id': [('zipcode', '=', self.zip)]}
        }

    @api.multi
    def toggle_active(self):
        self.ensure_one()
        self.active = False if self.active else True

    @api.multi
    def toggle_lock(self):
        self.ensure_one()
        self.is_lock = False if self.is_lock else True

    @api.multi
    def action_inhabitant(self):
        self.ensure_one()
        owner = self.mapped('lot_ids').mapped('owner_ids')
        loaner = self.mapped('lot_ids').mapped('loaner_ids')
        if self._context.get('inhabitant_type') == 'owner':
            action = self.env.ref('syndic_base.action_proprietaire').read()[0]
        elif self._context.get('inhabitant_type') == 'loaner':
            action = self.env.ref('syndic_base.action_locataire').read()[0]
        else:
            action = self.env.ref('base.action_partner_form').read()[0]
            action['domain'] = [('id', 'in', (owner | loaner).ids)]
            action['context'] = False

        return action

    @api.multi
    def action_lot(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').read()[0]
        action['domain'] = [('id', '=', self.lot_ids.ids)]
        return action

    def _get_quotity(self):
        for building in self:
            building.total_quotites = sum(building.mapped('lot_ids.quotities'))
            building.lot_count = len(building.lot_ids)
            building.owner_count = len(building.mapped('lot_ids.owner_ids'))
            building.loaner_count = len(building.mapped('lot_ids.loaner_ids'))


class Contractual(models.Model):
    _name = 'res.partner.contractual'
    _description = 'Contractual'

    is_contractual = fields.Boolean('Contractuelle')
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 domain=[('supplier', '=', True)])
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    partner_street = fields.Char(related='partner_id.street', string='Adresse')
    partner_zip = fields.Char(related='partner_id.zip', string='Code Postal')
    partner_city_id = fields.Many2one(related='partner_id.city_id',
                                      string='Ville')
    partner_phone = fields.Char(related='partner_id.phone', string='Téléphone')
    partner_email = fields.Char(related='partner_id.email', string='Email')

    @api.onchange('partner_id')
    def onchange_partner(self):
        return {
            'domain': {
                'partner_id': [
                    ('building_ids', 'not in', self.building_id.supplier_ids.ids),
                    ('supplier', '=', True),
                    ]
                }
        }

    @api.onchange('building_id')
    def onchange_building(self):
        return {
            'domain': {
                'building_id': [
                    ('id', 'not in', self.partner_id.building_ids.mapped('building_id').ids),
                    ]
                }
        }
