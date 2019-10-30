# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_locataire = fields.Boolean('Locataire', compute='_get_partner_type', store=True)
    is_proprietaire = fields.Boolean('Propriétaire', compute='_get_partner_type', store=True)
    is_old = fields.Boolean('Ancien propriétaire', compute='_get_partner_type', store=True)
    supplier = fields.Boolean('Fournisseur')

    mobile = fields.Char('GSM')
    fax = fields.Char('fax')

    job_ids = fields.Many2many('res.partner.job', string='Métier(s)')

    first_name = fields.Char('Prénom')
    convocation = fields.Selection([
        ('recommende', 'Par recommandé'),
        ('courrier_simple', 'Par courrier simple'),
        ('email', 'Par Email')
    ], string='Convocation')

    is_letter = fields.Boolean('Par Lettre')
    is_email = fields.Boolean('Par Email')

    lot_ids = fields.One2many('syndic.lot', 'owner_id', string='Lots')
    lot_count = fields.Integer('Quotitees Totales', compute='_get_number_lot')

    loaner_lot_ids = fields.Many2many('syndic.lot', 'lot_locataire', string='Lots(Locataire')
    loaner_lot_count = fields.Integer('Lots(Locataire)', compute='_get_number_lot_loaner')

    old_lot_ids = fields.Many2many('syndic.lot', 'old_prop_table', 'lot_id', 'old_proprio_id', string='Ancien lot')
    old_lot_count = fields.Integer('Ancien Lots', compute='_get_number_lot_old')

    owner_building_ids = fields.Many2many(
        'syndic.building', compute='_get_building', search='_search_building', string='Immeuble')
    loaner_building_ids = fields.Many2many(
        'syndic.building', compute='_get_building', search='_search_loaner_building', string='Immeuble(Locataire)')

    country_id = fields.Many2one('res.country', default=lambda s: s.env.ref('base.be'))
    building_ids = fields.One2many('res.partner.contractual', 'partner_id', string="Immeubles")
    quotity_line_ids = fields.Many2many('syndic.quotite.line', string='Quotitées')

    is_unindivision = fields.Boolean('Indivision')
    unindivision_ids = fields.Many2many('res.partner', 'res_partner_unindivision_rel', 'unindivision_id', 'partner_id', string="indivision")
    main_partner_id = fields.Many2one('res.partner', string="Contact Principale")

    @api.onchange('is_unindivision')
    def onchange_is_unindivision(self):
        if self.is_unindivision:
            self.email = ''
            self.first_name = ''
            self.title = False
            self.convocation = False
            self.phone = ''
            self.fax = ''
            self.mobile = ''
            self.zip = ''
            self.street = ''

    @api.onchange('main_partner_id', 'unindivision_ids')
    def onchange_undivision(self):
        if self.main_partner_id and self.unindivision_ids:
            all_name = '%s/%s' % (self.main_partner_id.name, '/'.join(self.unindivision_ids.mapped('name')))
            self.name = 'INDIVISION %s C/O %s' % (all_name, self.main_partner_id.name)

    def _get_name(self):
        if self._context.get('standard'):
            return super(Partner, self)._get_name()
        return self.name

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
        field = 'lot_ids.building_id.name'
        if isinstance(value, int):
            field = 'lot_ids.building_id.id'
        return [(field, operator, value)]

    def _search_loaner_building(self, operator, value):
        return [('loaner_lot_ids.building_id.id', operator, value)]

    def _get_building(self):
        for partner in self:
            partner.owner_building_ids = partner.lot_ids.building_id
            partner.loaner_building_ids = partner.loaner_lot_ids.building_id

    @api.model
    def create(self, vals):
        partner = super(Partner, self).create(vals)
        if not self._context.get('normal_create'):
            company_ids = self._context.get('allowed_company_ids')
            if not company_ids:
                company_ids = [self.env.ref('base.main_company').id]
            self.env['res.users'].with_context(normal_create=True).create({
                'partner_id': partner.id,
                'name': partner.name,
                'login': '%s - %s' % (partner.name, partner.id),
                'company_id': company_ids[0] if company_ids else False,
                'company_ids': [(6, 0, company_ids)],
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
            })
        return partner

    def write(self, vals):
        if vals.get('company_id') and vals['company_id'] != 1:
            del vals['company_id']
        return super().write(vals)

    @api.depends('lot_ids', 'loaner_lot_ids', 'loaner_lot_ids.building_id.active', 'lot_ids.building_id.active', 'old_lot_ids', 'lot_ids.owner_id')
    def _get_partner_type(self):
        for partner in self:
            if partner.lot_ids.filtered(lambda s: s.building_id.active):
                partner.is_proprietaire = True
            else:
                partner.is_proprietaire = False

            if partner.lot_ids.filtered(lambda s: not s.building_id.active) or partner.old_lot_ids:
                partner.is_old = True
            else:
                partner.is_proprietaire = False

            if partner.loaner_lot_ids and partner.loaner_lot_ids.building_id.active:
                partner.is_locataire = True
            else:
                partner.is_proprietaire = False

    def _get_sending_contact(self, email, letter):
        contacts = self.env['res.partner']
        for partner in self:
            if partner.is_unindivision:
                if partner.main_partner_id:
                    contacts |= partner.main_partner_id
                else:
                    contacts |= partner.unindivision_ids
            else:
                contacts |= partner

            if letter:
                contacts |= partner.child_ids.filtered(lambda s: s.is_letter)

            if email:
                contacts |= partner.child_ids.filtered(lambda s: s.is_email)

        return contacts

    @api.onchange('zip', 'country_id')
    def _onchange_zip(self):
        domain = [('country_id', '=', self.country_id.id)]
        if self.country_id.id == self.env.ref('base.be').id:
            domain.append(('zipcode', '=', self.zip))
        return {
            'domain': {'city_id': domain}
        }

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
    _description = 'Jobs'
    _order = 'name'

    name = fields.Char('Métier', requiered=True)


class Title(models.Model):
    _inherit = 'res.partner.title'
    _order = 'name'
