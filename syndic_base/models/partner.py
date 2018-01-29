# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, SUPERUSER_ID


class Partner(models.Model):
    _inherit = 'res.partner'

    is_locataire = fields.Boolean('Locataire', compute='_get_partner_type', store=True)
    # is_fournisseur = fields.Boolean('Fournisseur')
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

    lot_ids = fields.Many2many('syndic.lot', 'lot_proprietaire', string='Lot')
    loaner_lot_ids = fields.Many2many('syndic.lot', 'lot_locataire', string='Lot')

    building_ids = fields.Many2one('syndic.building', related='lot_ids.building_id', string='Immeuble non-storé')
    building_store_ids = fields.Many2one('syndic.building', related='lot_ids.building_id',
                                         string='Immeuble', store=True)

    loaner_building_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id',
                                          string='Immeuble non-storé')
    loaner_building_store_ids = fields.Many2one('syndic.building', related='loaner_lot_ids.building_id',
                                                string='Immeuble', store=True)

    old_lot_ids = fields.Many2many('syndic.lot', 'old_prop_table',
                                   'lot_id', 'old_proprio_id', string='Ancien lot')

    @api.model
    def create(self, vals):
        partner = super(Partner, self).create(vals)

        self.env['res.users']._signup_create_user({
            'partner_id': partner.id,
            'name': partner.name,
            'login': '%s - %s' % (partner.name, partner.id),
        })

        return partner


    @api.multi
    @api.depends('lot_ids', 'loaner_lot_ids', 'lot_ids.building_id.active', 'old_lot_ids')
    def _get_partner_type(self):
        for partner in self:
            building = partner.lot_ids.mapped('building_id') if partner.lot_ids else False
            if building:
                partner.is_proprietaire = True if partner.lot_ids and any(building.mapped('active')) else False
                partner.is_old = True if partner.old_lot_ids or False in building.mapped('active') else False
            partner.is_locataire = True if partner.loaner_lot_ids else False


class ResPartnerJob(models.Model):
    _name = 'res.partner.job'
    _order = 'name'

    name = fields.Char('Métier', requiered=True)


class Title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'
