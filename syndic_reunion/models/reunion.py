# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class ReunionListePresence(models.Model):
    _name = 'letter.reunion.list'
    _description = 'letter.reunion.list'
    _rec_name = 'reunion_id'
    
    reunion_id = fields.Many2one('letter.reunion', 'Reunion')
    partner_id = fields.Many2one('res.partner', 'Propriétaire')
    is_present = fields.Boolean('Présent')
    is_represente = fields.Boolean('Représenté')
    owner_id = fields.Many2one('res.partner', 'Représenté par', domain="[('is_proprietaire', '=', True)]")
    description = fields.Char('Description')

    def set_present(self):
        self.ensure_one()
        self.is_present = False if self.is_present else True

class LetterReunion(models.Model):
    _name = 'letter.reunion'
    _description = 'letter.reunion'
    _order = 'create_date desc'

    name = fields.Char(u'Réunion', compute="_get_name")
    immeuble_id = fields.Many2one('syndic.building', 'Immeuble', required=True)
    descriptif = fields.Html('Descriptif')
    point_ids = fields.One2many('reunion.point', 'reunion_id', 'Points')
    create_date = fields.Datetime(u'Date de création', readonly=True)
    write_date = fields.Datetime('Write Date', readonly=True)
    type_id = fields.Many2one('reunion.type', 'Type', required=True)
    date = fields.Date(u'Date d\'envoi', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date', store=True)

    owner_ids = fields.Many2many('res.partner', string='Liste de présence')
    percentage_present = fields.Float('Pourcentage de participation', compute="_get_percentage")
    percentage_quotity_present = fields.Float('Pourcentage de participation par quotitée', compute="_get_percentage_quotity")
    present_quotity = fields.Float('Quotitée Totale', compute="_get_percentage_quotity")

    list_ids = fields.One2many('letter.reunion.list', 'reunion_id', 'Liste de présence')

    state = fields.Selection(
        [
            ('draft', 'Ouvert'),
            ('list', 'Liste de Présence'),
            ('busy', 'En cours'),
            ('end', 'Cloturé')
        ], 'State', default="draft")

    def set_list(self):
        self.ensure_one()
        self.state = 'list'

    def set_busy(self):
        self.ensure_one()
        self.state = 'busy'

    def set_end(self):
        self.ensure_one()
        self.state = 'end'

    def open_points(self):
        action = self.env.ref('syndic_reunion.rapport_point').read()[0]
        action['domain'] = [('id', 'in', self.point_ids.ids)]
        return action

    def open_list(self):
        action = self.env.ref('syndic_reunion.rapport_presence_list').read()[0]
        action['domain'] = [('id', 'in', self.list_ids.ids)]
        return action

    def _get_name(self):
        for reunion in self:
            reunion.name = '%s %s %s' % (reunion.type_id.name, reunion.immeuble_id.name, reunion.date_fr)

    @api.depends('owner_ids')
    def _get_percentage_quotity(self):
        for reunion in self:
            total = sum(reunion.immeuble_id.lot_ids.mapped('quotity'))
            lots = reunion.immeuble_id.lot_ids & reunion.owner_ids.mapped('lot_ids')
            partial = sum(lots.mapped('quotity'))

            reunion.present_quotity = partial
            reunion.percentage_quotity_present = (partial/total)*100 if total else 0.00

    @api.depends('owner_ids')
    def _get_percentage(self):
        for reunion in self:
            total = len(self.immeuble_id.lot_ids.mapped('owner_ids'))
            partial = len(reunion.owner_ids)

            reunion.percentage_present = (partial/total)*100 if total else 0.00

    @api.onchange('immeuble_id')
    def _onchange_immeuble(self):
        owners = self.immeuble_id.lot_ids.mapped('owner_id')
        self.owner_ids = owners

        list_ids = [(6, 0, [])]
        for partner in owners:
            list_ids.append((0, 0, {'partner_id': partner.id}))

        self.list_ids = list_ids
        return {
            'domain': {
                'owner_ids': [('id', 'in', owners.ids)],
            }
        }

    @api.depends('date')
    def _compute_date(self):
        for rec in self:
            if rec.date:
                rec.date_fr = SyndicTools().french_date(rec.date)


class ReunionType(models.Model):
    _name = 'reunion.type'
    _description = 'reunion.type'

    name = fields.Char('Type', required=True)


class ReunionPoint(models.Model):
    _name = 'reunion.point'
    _description = 'reunion.point'
    _order = 'sequence'

    @api.model
    def _get_reunion_id(self):
        if self._context and self._context.get('active_id'):
            return self._context.get('active_id')

    name = fields.Char('Point', required=True)
    sequence = fields.Integer(u'Numéros de point')
    reunion_id = fields.Many2one('letter.reunion', 'Reunion', default=lambda s: s._get_reunion_id())
    descriptif = fields.Html('Description')

    quotity_id = fields.Many2one('syndic.quotite', string='Quotitée')

    acceptation_percentage = fields.Selection([
        ('50', '50%'),
        ('67', '2/3'),
        ('80', '4/5'),
        ('100', '100%'),
    ])

    is_vote = fields.Boolean('Est à voter')
    vote_ids = fields.One2many('syndic.vote', 'point_id', 'Votes')

    ok_vote = fields.Float('Vote OK', compute="_get_vote")
    final_vote = fields.Boolean('Vote final', compute="_get_final_vote")

    task_ids = fields.Many2many('syndic.claim', string="Tasks")

    def set_is_vote(self):
        self.ensure_one()
        self.is_vote = True

    @api.depends('vote_ids')
    def _get_vote(self):
        for point in self:
            point.ok_vote = sum(point.vote_ids.filtered(lambda s:s.vote == "ok").mapped('quotity_percentage'))

    @api.depends('vote_ids', 'acceptation_percentage')
    def _get_final_vote(self):
        for point in self:
            point.final_vote = point.ok_vote > float(point.acceptation_percentage)

    @api.onchange('reunion_id', 'name')
    def _onchange_reunion(self):
        return {
            'domain': {
                'quotity_id': [('building_id', '=', self.reunion_id.immeuble_id.id)]
            }
        }

    # def _get_owner_lot(self, partners):
    #     partner_lot = {}
    #     for partner in partners:
    #         partner_lot[partner] = 
            

    def _test(self):
        partner_lot = {}
        for lot in self.quotity_id.line_ids.mapped('lot_id'):
            partner_lot[lot.owner_ids] = lot

        return partner_lot

    @api.onchange('quotity_id')
    def _onchange_vote(self):
        values = [(6,0, [])]
        print(self._test())
        # for quotity in self.quotity_id

        for owner in self.quotity_id.line_ids.mapped('lot_owner_ids'):
            
            if owner in self.reunion_id.list_ids.mapped('partner_id'):
                quotity_lines = owner.quotity_line_ids.filtered(lambda s:s.quotity_id == self.quotity_id)
                
                lots = quotity_lines.mapped('lot_id').filtered(lambda s: s.building_id == self.reunion_id.immeuble_id)

                values.append([0, 0, {
                    'owner_id': owner.id,
                    'lot_ids': lots.ids,
                    'value': sum(quotity_lines.mapped('value')),
                    'vote': 'nok',
                }])

        self.vote_ids = values
        

class VotePerson(models.Model):
    _name = "syndic.vote"
    _description = "Vote"

    point_id = fields.Many2one('reunion.point', 'Points')
    
    owner_id = fields.Many2one('res.partner', 'Propriétaire')
    lot_ids = fields.Many2many('syndic.lot', string='Lots')

    value = fields.Float('Quotitées')
    quotity_percentage = fields.Float('Quotitées Pourcentage', compute="_get_quotity_percentage")

    vote = fields.Selection([
        ('ok', 'ok'),
        ('nok', 'Not ok'),
        ('abstention', 'Abstention'),
    ], 'Vote')

    def set_is_ok(self):
        self.ensure_one()
        self.vote = 'ok'

    def set_is_abstention(self):
            self.ensure_one()
            self.vote = 'abstention'

    def set_is_nok(self):
            self.ensure_one()
            self.vote = 'nok'

    @api.depends('value')
    def _get_quotity_percentage(self):
        for vote in self:
            total = vote.point_id.reunion_id.present_quotity
            partial = vote.value

            vote.quotity_percentage = (partial/total)*100 if total else 0.00
