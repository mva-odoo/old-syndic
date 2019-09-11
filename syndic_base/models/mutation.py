# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Mutation(models.Model):
    _name = 'syndic.mutation'
    _description = 'Mutation'
    _order = 'immeuble_id'

    name = fields.Char('Mutation', compute='_get_name', store=True)
    mutation_date = fields.Date('Date de mutation')
    old_owner_ids = fields.Many2many('res.partner', 'old_owner_table', string='Ancien Propriétaire', required=True)
    new_owner_id = fields.Many2one('res.partner', string='Nouveau Propriétaire', required=True)
    lot_ids = fields.Many2many('syndic.lot', string='Lot', required=True)
    state = fields.Selection([('draft', 'brouillon'), ('done', 'terminé')], 'Etat', default='draft')
    immeuble_id = fields.Many2one('syndic.building', related='lot_ids.building_id', store=True, string="Immeuble")

    @api.depends('old_owner_ids', 'new_owner_id')
    def _get_name(self):
        for mutation in self:
            mutation.name = 'Mutation de %s vers %s' % (
                ''.join(mutation.old_owner_ids.mapped('name')),
                mutation.new_owner_id.name
            )

    @api.onchange('old_owner_ids')
    def onchange_old_owner(self):
        return {
            'domain': {
                    'lot_ids': [('owner_id', 'in', self.old_owner_ids.ids)]
                }
        }

    def mutation(self):
        if not self.env.context.get('no_mutation', False):
            for mutation in self:
                mutation.old_owner_ids.write({'old_lot_ids': [(4, lot_id.id) for lot_id in mutation.lot_ids]})
                mutation.lot_ids.write({'owner_id': self.new_owner_id.id})

                if not mutation.old_owner_ids.mapped('lot_ids.owner_id'):
                    mutation.old_owner_ids.mapped('user_id').write({'active': False})

                mutation.write({'state': 'done'})

                old_owner_name = mutation.old_owner_ids.mapped('name')
                for lot in mutation.lot_ids:
                    lot.message_post(
                        body=_('Mutation le %s: <b>Ancien:</b> %s - <b>Nouveau:</b> %s' % (
                            mutation.mutation_date,
                            ', '.join(old_owner_name),
                            mutation.new_owner_id.name,
                        ))
                )
        else:
            return {}

