# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.addons.syndic_tools.syndic_tools import SyndicTools


class CreateLetter(models.Model):
    _name = 'letter.letter'
    _description = 'letter.letter'
    _rec_name = 'sujet'
    _order = 'date desc'

    name = fields.Char('ID de la lettre', readonly=True)
    sujet = fields.Char('Sujet', required=True)
    immeuble_id = fields.Many2one('syndic.building', string='Immeuble')
    all_immeuble = fields.Boolean('Immeuble entier')
    propr_ids = fields.Many2many(
                            'res.partner',
                            'res_partner_owner_rel',
                            'id1',
                            'id2',
                            domain=[('is_proprietaire', '=', True)],
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

    all_partner_ids = fields.Many2many('res.partner', string='All Partner',
                                       compute='_get_all_partner')
    end_letter_id = fields.Many2one('letter.end', 'Fin de lettre', required=True)
    begin_letter_id = fields.Many2one('letter.begin', u'Début de lettre', required=True)
    letter_type_id = fields.Many2one('letter.type', 'Type de lettre', required=True)
    letter_model_id = fields.Many2one('letter.model', u'Modèle de lettre')
    contenu = fields.Html('contenu', required=True)
    ps = fields.Text('PS')
    is_mail = fields.Boolean('Envoi par email')
    is_fax = fields.Boolean('Envoi par fax')
    piece_jointe_ids = fields.Many2many('ir.attachment', 'letter_id', string='Piece Jointe')
    create_date = fields.Datetime(u'Date de création')
    date = fields.Date(u'Date de création', default=lambda *a: fields.date.today(), copy=False)
    date_fr = fields.Char(string='Date', compute='_compute_date')
    partner_address_ids = fields.Many2many(
        'res.partner',
        String="Personne Jointe",
        compute='_compute_join_address')
    state = fields.Selection([('not_send', 'Pas envoyé'), ('send', 'Envoyé')], string='State', default='not_send')
    mail_server = fields.Many2one('ir.mail_server', 'Serveur email')

    @api.multi
    def _get_all_partner(self):
        for letter in self:
            letter.all_partner_ids = letter.propr_ids | letter.fourn_ids | letter.divers_ids | letter.loc_ids | letter.divers_ids | letter.partner_address_ids

    @api.multi
    def save_template(self):
        return {
            'name': 'Sauver comme modèle',
            'type': 'ir.actions.act_window',
            'res_model': 'syndic.template.mail',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.one
    @api.depends('date')
    def _compute_date(self):
        if self.date:
            self.date_fr = SyndicTools().french_date(self.date)

    @api.model
    def create(self, vals):
        res = super(CreateLetter, self).create(vals)

        for supplier_id in res.fourn_ids:
            values = {
                'name': res.sujet,
                'fournisseur_id': supplier_id.id,
                'immeuble_id': res.immeuble_id.id,
            }

            if res.letter_type_id.name in ['Demande de devis', 'Demande d\'offre', 'Demande de contrat']:
                values['date_envoi'] = res.date
                self.env['offre.contrat'].create(values)

            elif res.letter_type_id.name in ['Bon de commande']:
                values['date_demande'] = res.date
                self.env['bon.commande'].create(values)
        return res

    @api.onchange('is_mail')
    def onchange_server(self):
        self.mail_server = self.env.user.server_mail_id.id if self.is_mail else False

    @api.onchange('immeuble_id', 'all_immeuble')
    def onchange_immeuble(self):
        self.propr_ids = self.immeuble_id.mapped('lot_ids.owner_ids') if self.all_immeuble else self.env['res.partner']

    @api.depends('propr_ids', 'fourn_ids', 'loc_ids')
    def _compute_join_address(self):
        self.partner_address_ids = self.all_partner_ids.mapped('child_ids').filtered(lambda s: s.is_letter)
        self.is_fax = True if self.fourn_ids else False

    @api.one
    def send_email_lettre(self):
        header = ''

        mail = {
            'mail_server_id': self.mail_server if self.mail_server else self.env.user.server_mail_id or False,
            'email_from': self.env.user.email,
            'reply_to': self.env.user.email,
            'attachment_ids': [(6, 0, self.piece_jointe_ids.ids)],
            'subject': self.immeuble_id.name + '-' + self.sujet if self.immeuble_id else self.sujet,
        }

        if self.immeuble_id:
            header = "Concerne %s<br/>%s<br/>%s %s<br/><br/>" % (self.immeuble_id.name,
                                                                 self.immeuble_id.address_building,
                                                                 str(self.immeuble_id.zip_building),
                                                                 str(self.immeuble_id.city_building.name))

        body = "%s<br/>%s<br/>Cordialement.<br/><br/>" % (self.begin_letter_id.name, self.contenu)

        footer = """<br/>L'&eacute;quipe SG IMMO<br/>
Rue Fran&ccedil;ois Vander Elst, 38/1<br/>
1950 Kraainem<br/>
'<img src="https://lh6.googleusercontent.com/-7QA8bP7oscU/UUrXkQ1-rHI/AAAAAAAAAAk/WhbiGpLAUCQ/s270/Logo_SG%2520immo.JPG"
width="96" height="61"/>'"""

        mail['body_html'] = header + body + self.ps + '<br/>'+footer if self.ps else header + body + footer

        for prop in self.propr_ids.filtered(lambda s: s.email):
            mail['email_to'] = prop.email
            self.env['mail.mail'].create(mail)

        for fourn in self.fourn_ids.filtered(lambda s: s.email):
            mail['email_to'] = fourn.email
            self.env['mail.mail'].create(mail)

        for loc in self.loc_ids.filtered(lambda s: s.email):
            mail['email_to'] = loc.email
            self.env['mail.mail'].create(mail)

        for div in self.divers_ids.filtered(lambda s: s.email):
            mail['email_to'] = div.email
            self.env['mail.mail'].create(mail)

        for addr in self.propr_ids.mapped('child_ids').filtered(lambda s: s.email and s.is_email):
            mail['email_to'] = addr.email
            self.env['mail.mail'].create(mail)

        self.write({
            'is_mail': True,
            'state': 'send',
        })

    @api.onchange('letter_model_id')
    def onchange_letter(self):
        self.contenu = self.letter_model_id.text


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
