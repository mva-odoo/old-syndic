# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Mutation(models.Model):
    _name = 'syndic.mutation'
    _description = 'Mutation'
    _order = 'immeuble_id'

    name = fields.Char('Mutation', compute='_get_name', store=True)
    mutation_date = fields.Date('Date de mutation')
    old_owner_ids = fields.Many2many('res.partner', 'old_owner_table', string='Ancien Propriétaire', required=True)
    new_owner_ids = fields.Many2many('res.partner', 'new_owner_table', string='Nouveau Propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot', required=True)
    state = fields.Selection([('draft', 'brouillon'), ('done', 'terminé')], 'Etat', default='draft')
    immeuble_id = fields.Many2one('syndic.building', related='lot_ids.building_id', store=True, string="Immeuble")

    @api.multi
    @api.depends('old_owner_ids', 'new_owner_ids')
    def _get_name(self):
        for mutation in self:
            mutation.name = 'Mutation de %s vers %s' % (
                ''.join(mutation.old_owner_ids.mapped('name')),
                ''.join(mutation.new_owner_ids.mapped('name'))
            )

    @api.onchange('old_owner_ids')
    def onchange_old_owner(self):
        return {
            'domain': {'lot_ids': [('owner_ids', 'in',  self.old_owner_ids.ids)]}
        }

    @api.multi
    def mutation(self):
        if not self.env.context.get('no_mutation', False):
            for mutation in self:
                mutation.old_owner_ids.write({'old_lot_ids': [(4, lot_id.id) for lot_id in mutation.lot_ids]})
                mutation.lot_ids.write({'owner_ids': [(6, 0, self.new_owner_ids.ids)]})

                if not mutation.old_owner_ids.mapped('lot_ids.owner_ids'):
                    mutation.old_owner_ids.mapped('user_id').write({'active': False})

                mutation.write({'state': 'done'})

                mutation.lot_ids.message_post(
                    body=_('Mutation le %s: Ancien: %s - Nouveau %s' % (
                        mutation.mutation_date,
                        mutation.old_owner_ids.mapped('name'),
                        mutation.new_owner_ids.mapped('name'),
                    ))
                )
        else:
            # just save in draft
            return {}

