# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Immeuble(models.Model):
    _name = 'syndic.building'
    _description = 'Immeubles'
    _order = 'name asc'

    name = fields.Char('Immeuble', required=True)
    active = fields.Boolean(default=True)

    BCE = fields.Char('BCE')
    num = fields.Integer(u"N°", required=True)
    street = fields.Char('Rue', required=True)
    zip = fields.Integer('Code Postal', required=True)
    compte = fields.Char('Compte en banque')

    city_id = fields.Many2one('res.partner.city', 'Commune', required=True)
    supplier_ids = fields.Many2many('res.partner', string="Fiche technique")
    total_quotites = fields.Float(compute='_get_quotity', string='Total des Quotitées')

    lot_ids = fields.One2many('syndic.lot', 'building_id', 'Lots')
    lot_count = fields.Integer(compute='_get_quotity', string='Nombre de lots')

    owner_count = fields.Integer(compute='_get_quotity', string='Nombre de Propriétaires')
    loaner_count = fields.Integer(compute='_get_quotity', string='Nombre de Locataires')

    note = fields.Text('Notes')

    honoraire = fields.Float('Honoraire', groups='syndic_management.syndic_manager')
    frais_admin = fields.Float('Frais Administratif', groups='syndic_management.syndic_manager')

    manager_id = fields.Many2one('res.users', 'Manager',
                                 domain="[('groups_id.name','in',['Syndic/Employe','Syndic/Manager'])]")

    is_private_gestion = fields.Boolean("Gestion Privative")
    is_lock = fields.Boolean('Bloquer')

    signalitic_id = fields.Many2one('syndic.building.signalitic', string='Immeuble',
                    required=True, ondelete="cascade", delegate=True)
    sign_mois_rel = fields.Selection(string='Mois', related='signalitic_id.date_mois')
    sign_quizaine_rel = fields.Selection(string='Quinzaine', related='signalitic_id.date_quizaine')

    @api.model
    def create(self, vals):
        vals['is_lock'] = True
        return super(Immeuble, self).create(vals)

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

    @api.depends('lot_ids')
    def _get_quotity(self):
        for building in self:
            building.total_quotites = sum(building.mapped('lot_ids.quotities'))
            building.lot_count = len(building.lot_ids)
            building.owner_count = len(building.mapped('lot_ids.owner_ids'))
            building.loaner_count = len(building.mapped('lot_ids.loaner_ids'))

    def open_tech(self):
        self.ensure_one()
        action = self.env.ref('syndic_base.action_signalitic').read()[0]
        action['res_id'] = self.signalitic_id.id
        return action
