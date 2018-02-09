# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, SUPERUSER_ID


class Partner(models.Model):
    _inherit = 'res.partner'

    is_locataire = fields.Boolean('Locataire', compute='_get_partner_type', store=True)
    is_proprietaire = fields.Boolean('Propriétaire', compute='_get_partner_type', store=True)
    is_old = fields.Boolean('Ancien propriétaire', compute='_get_partner_type', store=True)

    city_id = fields.Many2one('res.partner.city', 'Ville')
    mobile = fields.Char('GSM')
    fax = fields.Char('fax')

    job_ids = fields.Many2many('res.partner.job', string='Métier(s)')

    first_name = fields.Char('Prénom')
    convocation = fields.Selection([
        ('recommende', 'Par recommandé'),
        ('courrier_simple', 'Par courrier simple'),
        ('email', 'Par Email')
    ], string='Convocation')

    is_letter = fields.Boolean('Lettre')
    is_email = fields.Boolean('Email')

    lot_ids = fields.Many2many('syndic.lot', 'lot_proprietaire', string='Lots')
    lot_count = fields.Integer('Lots', compute='_get_number_lot')

    loaner_lot_ids = fields.Many2many('syndic.lot', 'lot_locataire', string='Lots(Locataire')
    loaner_lot_count = fields.Integer('Lots(Locataire)', compute='_get_number_lot_loaner')

    old_lot_ids = fields.Many2many('syndic.lot', 'old_prop_table', 'lot_id', 'old_proprio_id', string='Ancien lot')
    old_lot_count = fields.Integer('Ancien Lots', compute='_get_number_lot_old')

    building_ids = fields.Many2many('syndic.building', compute='_get_building',
                                    search='_search_building', string='Immeuble')
    loaner_building_ids = fields.Many2many('syndic.building', compute='_get_building',
                                           search='_search_loaner_building', string='Immeuble(Locataire)')

    @api.depends('lot_ids')
    def _get_number_lot(self):
        for partner in self:
            partner.lot_count = len(partner.lot_ids)

    @api.depends('loaner_lot_ids')
    def _get_number_lot_loaner(self):
        for partner in self:
            partner.loaner_lot_count = len(partner.loaner_lot_ids)

    @api.depends('old_lot_ids')
    def _get_number_lot_old(self):
        for partner in self:
            partner.old_lot_count = len(partner.old_lot_ids)

    def _search_building(self, operator, value):
        return [('lot_ids.building_id.name', operator, value)]

    def _search_loaner_building(self, operator, value):
        return [('loaner_lot_ids.building_id.name', operator, value)]

    @api.depends('lot_ids')
    def _get_building(self):
        for partner in self:
            partner.building_ids = partner.lot_ids.mapped('building_id')
            partner.loaner_building_ids = partner.loaner_lot_ids.mapped('building_id')

    @api.model
    def create(self, vals):
        partner = super(Partner, self).create(vals)
        if not self._context.get('normal_create'):
            self.env['res.users'].with_context(normal_create=False).create({
                'partner_id': partner.id,
                'name': partner.name,
                'login': '%s - %s' % (partner.name, partner.id),
            })
        return partner

    @api.depends(
        'lot_ids', 'loaner_lot_ids', 'loaner_lot_ids.building_id.active', 'lot_ids.building_id.active', 'old_lot_ids')
    def _get_partner_type(self):
        for partner in self:
            if partner.lot_ids.filtered(lambda s: s.building_id.active):
                partner.is_proprietaire = True

            if partner.lot_ids.filtered(lambda s: not s.building_id.active) or partner.old_lot_ids:
                partner.is_old = True

            if partner.loaner_lot_ids and partner.loaner_lot_ids.mapped('building_id').active:
                partner.is_locataire = True

    def action_lot(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').read()[0]
        action['domain'] = [('id', 'in', self.lot_ids.ids)]
        return action

    def action_lot_loaner(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').read()[0]
        action['domain'] = [('id', 'in', self.loaner_lot_ids.ids)]
        return action

    def action_lot_old(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_lot').read()[0]
        action['domain'] = [('id', 'in', self.old_lot_ids.ids)]
        return action


class ResPartnerJob(models.Model):
    _name = 'res.partner.job'
    _order = 'name'

    name = fields.Char('Métier', requiered=True)


class Title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'
