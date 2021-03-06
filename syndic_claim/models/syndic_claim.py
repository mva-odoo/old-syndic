# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions
from datetime import date


class Claim(models.Model):
    _name = 'syndic.claim'
    _description = 'Tache Syndic'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'subject'
    _order = 'create_date desc'

    active = fields.Boolean('Active', default=True)
    subject = fields.Char('Sujet', required=True)
    description = fields.Html('Description')
    create_date = fields.Datetime(string=u'Date de création', readonly=True)
    write_date = fields.Datetime(string='Update Date', readonly=True)
    create_uid = fields.Many2one('res.users', string="Createur", readonly=True)
    write_uid = fields.Many2one('res.users', string="Modifieur", readonly=True)
    manager_id = fields.Many2one('res.users', string='Manager de la plainte',
                                 domain=['!', ('groups_id.name', 'ilike', 'Syndic/Client')],
                                 default=lambda self: self.env.uid)
    
    owner_ids = fields.Many2many('res.partner',
                                 domain=[('is_proprietaire', '=', True)],
                                 string=u'Propriétaires')
    supplier_ids = fields.Many2many('res.partner',
                                    domain=[('supplier', '=', True)],
                                    string='Fournisseurs')
   
    claim_status_id = fields.Many2one('claim.status', string='Status de la plainte')
    building_id = fields.Many2one('syndic.building', 'Immeuble')
    importance = fields.Selection([('0', 'pas important'),
                                   ('1', 'important'),
                                   ('2', 'tres important'),
                                   ('3', 'ultra important')],
                                  string='Importance')
    color = fields.Integer('Color')

    type_id = fields.Many2one('claim.type', 'Type')

    @api.onchange('importance')
    def onchange_color(self):
        self.color = self.importance

    @api.multi
    def write(self, vals):
        for res in self:
            partners = res.owner_ids | res.supplier_ids | res.manager_id.partner_id
            res.message_subscribe(partner_ids=partners.ids)
        return super(Claim, self).write(vals)

    @api.model
    def create(self, vals):

        res = super(Claim, self).create(vals)
        partners = res.owner_ids | res.supplier_ids | res.manager_id.partner_id
        res.message_subscribe(partner_ids=partners.ids)
        if res.manager_id.id != res.create_uid.id:
            
            body = """Bonjour,
une tâche t'attends sur : <a href='https://sgimmo.be/web#id=%i&view_type=form&model=syndic.claim&menu_id=128&action=119'>Odoo</a>
""" % res.id
            res.message_post(partner_ids= res.manager_id, body=body, subject="Une tâche t\'attends dans Odoo", message_type="email")

            # self.env['mail.mail'].create({
            #     'mail_server_id':  self.env.user.server_mail_id.id or False,
            #     'email_from': self.env.user.email,
            #     'reply_to': self.env.user.email,
            #     'body_html': body,
            #     'subject': 'Une tâche t\'attends dans Odoo',
            #     'email_to': self.env['res.users'].browse(vals.get('manager_id')).email
            # })

        return res


class ClaimStatus(models.Model):
    _name = 'claim.status'
    _description = 'claim.status'

    name = fields.Char('Status', required=True)
    sequence = fields.Integer('Status sequence')


class ClaimType(models.Model):
    _name = 'claim.type'
    _description = 'claim.type'

    name = fields.Char('Status', required=True)


class CommentHistory(models.Model):
    _name = 'comment.history'
    _description = 'comment.history'
    _rec_name = 'description'

    create_date = fields.Datetime(u'Date de création', readonly=True)
    write_date = fields.Datetime('Date de modification', readonly=True)
    create_uid = fields.Many2one('res.users', string="Create User", readonly=True)
    write_uid = fields.Many2one('res.users', string="Write User", readonly=True)
    description = fields.Text('Texte')
    current_status = fields.Many2one('claim.status', string='Current status')
    claim_ids = fields.Many2one('syndic.claim', string='Claim')


class OffreContrats(models.Model):
    _name = 'offre.contrat'
    _description = 'offre.contrat'
    _order = 'date_envoi desc'

    name = fields.Char('Type', required=True)
    fournisseur_id = fields.Many2one('res.partner',
                                     domain=[('supplier', '=', True)],
                                     string='Nom du fournisseur',
                                     required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Nom immeuble', required=True)
    demande = fields.Selection([('offre', 'Offre'), ('contrat', 'Contrat')], string='Demande')
    date_envoi = fields.Date('Date envoi', required=True)
    envoi_par = fields.Selection([('recommende', 'Par recommandé'),
                                  ('courrier_simple', 'Par courrier simple'),
                                  ('email', 'Par Email'),
                                  ('fax', 'Par Fax')], string=u'Envoyé par')
    reception = fields.Boolean('Reception')
    date_reception = fields.Date('Date reception')
    transmition = fields.Boolean('Transmition')
    date_transmition = fields.Date('Date transmition')
    acceptation = fields.Boolean('Acceptaté')
    accept = fields.Selection([('accepte', 'Accepté'),
                               ('non_accpet', 'Pas accepté')], 'Acceptation')
    date_acceptation = fields.Date('Date acceptation')
    is_bon_commande = fields.Boolean('Bon de commande fait', default=False)
    is_refused = fields.Boolean('Refuser', default=False)

    @api.onchange('reception')
    def onchange_reception(self):
        self.date_reception = date.today().strftime('%Y-%m-%d') if self.reception else False

    @api.onchange('transmition')
    def onchange_transmition(self):
        self.date_transmition = date.today().strftime('%Y-%m-%d') if self.transmition else False

    @api.onchange('acceptation')
    def onchange_acceptation(self):
        self.date_acceptation = date.today().strftime('%Y-%m-%d') if self.acceptation else False

    @api.one
    def transform_bon_commande(self):
        self.env['bon.commande'].create({
            'name': self.name,
            'immeuble_id': self.immeuble_id.id,
            'fournisseur_id': self.fournisseur_id.id,
            'date_demande': self.date_acceptation,
        })
        self.is_bon_commande = True


class BonCommande(models.Model):
    _name = 'bon.commande'
    _description = 'bon.commande'
    _order = 'date_demande desc'

    name = fields.Char('Type', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Nom immeuble', required=True)
    fournisseur_id = fields.Many2one('res.partner',
                                     domain=[('supplier', '=', True)],
                                     string='Nom du fournisseur',
                                     required=True)
    date_demande = fields.Date('Date demande')
    cloture = fields.Boolean('Cloture')
    date_cloture = fields.Date('Date cloture')

    @api.onchange('cloture')
    def onchange_cloture(self):
        self.date_cloture = date.today().strftime('%Y-%m-%d') if self.cloture else False
