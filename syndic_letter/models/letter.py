# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class CreateLetter(models.Model):
    _name = 'letter.letter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'letter.letter'
    _rec_name = 'sujet'
    _order = 'date desc'

    send_ids = fields.Many2many(
        'letter.send', string='Type d\'envoi', required=True)

    name = fields.Char('ID de la lettre', readonly=True)
    sujet = fields.Char('Sujet', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble')
    user_from_id = fields.Many2one(
        'res.users',
        'From',
        required=True,
        default=lambda self: self.env.user,
        domain="[('groups_id.name','in',['Syndic/Employe','Syndic/Manager'])]"
    )
    all_immeuble = fields.Boolean('Immeuble entier')
    propr_ids = fields.Many2many(
                            'res.partner',
                            'res_partner_owner_rel',
                            'id1',
                            'id2',
                            domain=[('is_proprietaire', '=', True)],
                            compute='_get_immeuble',
                            readonly=False,
                            store=True,
                            string=u'Propriétaire')
    fourn_ids = fields.Many2many(
                            'res.partner',
                            'res_partner_supplier_rel',
                            'id1',
                            'id2',
                            domain=[('supplier', '=', True)],
                            string='Fournisseurs')
    divers_ids = fields.Many2many(
                            'res.partner',
                            'res_partner_other_rel',
                            'id1',
                            'id2',
                            string='Divers')
    old_ids = fields.Many2many(
                            'res.partner',
                            'res_partner_old_rel',
                            'id1',
                            'id2',
                            domain=[('is_old', '=', True)],
                            string=u'Ancien Propriétaire')
    loc_ids = fields.Many2many(
                            'res.partner',
                            'res_partner_loaner_rel',
                            'id1',
                            'id2',
                            domain=[('is_locataire', '=', True)],
                            string='Locataires')

    all_partner_ids = fields.Many2many(
        'res.partner', string='All Partner', compute='_get_all_partner')
    end_letter_id = fields.Many2one('letter.end', 'Fin de lettre')
    begin_letter_id = fields.Many2one('letter.begin', u'Début de lettre')
    letter_type_id = fields.Many2one(
        'letter.type', 'Type de lettre', required=True)
    letter_model_id = fields.Many2one(
        'letter.model',
        compute='_get_send_type',
        readonly=False,
        store=True,
        compute_sudo=False,
        string=u'Modèle de lettre',
    )
    contenu = fields.Html(
        'contenu',
        required=True,
        compute='_get_body',
        readonly=False,
        store=True
    )
    ps = fields.Text('PS')
    is_mail = fields.Boolean('Envoi par email', compute="_get_send_type")
    is_fax = fields.Boolean('Envoi par fax')
    piece_jointe_ids = fields.Many2many(
        'ir.attachment', 'letter_id', string='Piece Jointe')
    create_date = fields.Datetime(u'Date de création')
    date = fields.Date(
        u'Date d\'envoi',
        default=lambda *a: fields.date.today(),
        copy=False
    )
    date_fr = fields.Char(string='Date', compute='_compute_date')
    is_merge = fields.Boolean('Fusionner les Pièces jointes')
    state = fields.Selection(
        [
            ('not_send', 'Pas envoyé'),
            ('send', 'Envoyé')
        ],
        string='State',
        default='not_send'
    )

    mail_server = fields.Many2one(
        'ir.mail_server',
        compute='_get_mail_server',
        readonly=False,
        store=True,
        string='Serveur email',
    )

    mail_ids = fields.One2many('mail.mail', 'letter_id', 'Emails')

    @api.depends('send_ids')
    def _get_send_type(self):
        for letter in self:
            if any(letter.send_ids.mapped('is_email')):
                letter.is_mail = True
            else:
                letter.is_mail = False

            letter.letter_model_id = False
            for send_type in letter.send_ids:
                letter.letter_model_id = send_type.model_id

    @api.depends('propr_ids', 'fourn_ids', 'divers_ids', 'loc_ids', 'send_ids')
    def _get_all_partner(self):
        for letter in self:
            partners = letter.propr_ids | letter.fourn_ids | letter.loc_ids | letter.divers_ids
            is_mail = any(letter.send_ids.mapped('is_email'))
            is_papper = any(letter.send_ids.mapped('is_papper'))

            letter.all_partner_ids = partners._get_sending_contact(is_mail, is_papper)

    def save_template(self):
        return {
            'name': 'Sauver comme modèle',
            'type': 'ir.actions.act_window',
            'res_model': 'syndic.template.mail',
            'view_mode': 'form',
            'target': 'new',
        }

    def _compose_message_vals(self, template_id):
        child_partners = self.all_partner_ids.mapped('child_ids').filtered(lambda s: s.is_email)
        partners = self.all_partner_ids.filtered(lambda s: s.email) | child_partners

        return {
            'model': 'letter.letter',
            'res_id': self.id,
            'template_id': template_id,
            'mail_server_id': self.user_from_id.server_mail_id.id,
            'composition_mode': 'comment',
            'partner_ids': [(6, 0, partners.ids)],
        }

    def print_letter(self):
        for letter in self:
            res = []
            for send_type in letter.send_ids:
                if send_type.mycontext:
                    mycontext = eval(send_type.mycontext)
                    send_type = send_type.with_context(mycontext)

                if send_type.is_email:
                    template_id = send_type.mail_template_id
                    if template_id:
                        vals = letter._compose_message_vals(template_id.id)
                        mail = self.env['mail.compose.message'].create(vals)
                        mail.onchange_template_id_wrapper()
                        mail.send_mail()

                if send_type.is_papper:
                    res.append(send_type.action_id.id)

            if not letter.send_ids:
                raise exceptions.UserError(_("Il faut choisir un type de lettre"))
            return send_type.action_id.with_context(multi_report=res).report_action(letter)

    @api.depends('date')
    def _compute_date(self):
        for rec in self:
            if rec.date:
                rec.date_fr = SyndicTools().french_date(rec.date)

    @api.model
    def create(self, vals):
        res = super(CreateLetter, self).create(vals)

        for supplier_id in res.fourn_ids:
            values = {
                'name': res.sujet,
                'fournisseur_id': supplier_id.id,
                'immeuble_id': res.immeuble_id.id,
            }
            if not self.env.context.get('no_offer'):
                if res.letter_type_id.name in ['Demande de devis', 'Demande d\'offre', 'Demande de contrat']:
                    values['date_envoi'] = res.date
                    self.env['offre.contrat'].create(values)

                elif res.letter_type_id.name in ['Bon de commande']:
                    values['date_demande'] = res.date
                    self.env['bon.commande'].create(values)
        return res

    @api.depends('is_mail')
    def _get_mail_server(self):
        for letter in self:
            server_id = letter.env.user.server_mail_id.id
            letter.mail_server = server_id if letter.is_mail else False

    @api.depends('immeuble_id', 'all_immeuble')
    def _get_immeuble(self):
        for letter in self:
            owners = letter.env['res.partner']
            for owner in letter.immeuble_id.lot_ids.owner_id:
                if owner.is_unindivision:
                    if owner.main_partner_id:
                        owners |= owner.main_partner_id
                    else:
                        owners |= owner.unindivision_ids
                else:
                    owners |= owner

            letter.propr_ids = owners if letter.all_immeuble else False

    @api.depends('letter_model_id')
    def _get_body(self):
        for letter in self:
            if not letter.contenu:
                letter.contenu = letter.letter_model_id.text


class EndLetter(models.Model):
    _name = 'letter.end'
    _description = 'letter.end'

    name = fields.Char('Fin de lettre', required=True)


class BeginLetter(models.Model):
    _name = 'letter.begin'
    _description = 'letter.begin'

    name = fields.Char('Debut de lettre', required=True)


class LetterType(models.Model):
    _name = 'letter.type'
    _description = 'letter.type'

    name = fields.Char('Type Letter', required=True)


class LetterModel(models.Model):
    _name = 'letter.model'
    _description = 'letter.model'

    name = fields.Char('Model Letter', required=True)
    text = fields.Html('Text', required=True)


class LetterSend(models.Model):
    _name = 'letter.send'
    _description = 'letter.send'

    name = fields.Char('Model Letter', required=True)
    is_email = fields.Boolean('Email')
    is_papper = fields.Boolean('Papier')
    action_id = fields.Many2one('ir.actions.report', 'Action Rapport')
    mail_template_id = fields.Many2one('mail.template', 'Email Template')
    mycontext = fields.Char('Context à passer')
    model_id = fields.Many2one('letter.model', 'Modèle de Lettre')
