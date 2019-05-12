# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class LetterReunion(models.Model):
    _name = 'letter.reunion'
    _description = 'letter.reunion'
    _order = 'create_date desc'

    name = fields.Char(u'Réunion', required=True)
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

    @api.depends('owner_ids')
    def _get_percentage(self):
        for reunion in self:
            total = len(self.immeuble_id.lot_ids.mapped('owner_ids'))
            partial = len(reunion.owner_ids)

            reunion.percentage_present = (partial/total)*100 if total else 0.00

    @api.onchange('immeuble_id')
    def _onchange_immeuble(self):
        self.owner_ids = self.immeuble_id.lot_ids.mapped('owner_ids')
        
        return {
            'domain': {
                'owner_ids': [('id', 'in', self.owner_ids.ids)],
            }
        }

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = SyndicTools().french_date(self.date)


class ReunionType(models.Model):
    _name = 'reunion.type'
    _description = 'reunion.type'

    name = fields.Char('Type', required=True)


class ReunionPoint(models.Model):
    _name = 'reunion.point'
    _description = 'reunion.point'
    _order = 'sequence'

    name = fields.Char('Point', required=True)
    sequence = fields.Integer(u'Numéros de point')
    reunion_id = fields.Many2one('letter.reunion', 'Reunion')
    descriptif = fields.Html('Description')
    
    quotity_id = fields.Many2one('syndic.quotite', string='Quotitée')

    acceptation_percentage = fields.Selection([
        ('50', '50%'),
        ('2-3', '2/3'),
        ('4-5', '4/5'),
        ('100', '100%'),
    ])

    vote_ids = fields.One2many('syndic.vote', 'point_id', 'Votes')

    @api.onchange('reunion_id', 'name')
    def _onchange_reunion(self):
        return {
            'domain': {
                'quotity_id': [('building_id', '=', self.reunion_id.immeuble_id.id)]
            }
        }

    @api.onchange('quotity_id')
    def _onchange_vote(self):
        values = [(6,0, [])]
        for owner in self.quotity_id.line_ids.mapped('lot_owner_ids'):
            if owner in self.reunion_id.owner_ids:
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

    @api.depends('value')
    def _get_quotity_percentage(self):
        for vote in self:
            percentage = vote.point_id.reunion_id.percentage_present
            vote.quotity_percentage = vote.value + ((vote.value * 100-percentage)/100)/len(self.point_id.vote_ids)
