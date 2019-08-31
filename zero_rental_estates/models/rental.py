# -*- coding: utf-8 -*-

import re
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, tools, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import float_compare, pycompat
from odoo.addons import decimal_precision as dp


class Rental(models.Model):
    _name = 'lb.rental'
    _rec_name = 'estate_rented'

    estate_rented = fields.Many2one('lb.estate', ondelete='cascade', string="estate rented", required=True)
    partner = fields.Many2one('res.partner', ondelete='cascade', string="partner", required=True)
    rental_status = fields.Selection([('inactive', 'Inactive'),('active', 'active')], string="Statut", compute='update_statut', help="Statut de la rental (active : rental en cours)")
    utilization = fields.Selection([('utilization1', 'utilization main if partner'),('utilization2', 'utilization secondary of partner'),('utilization3', 'utilization professional')], string="utilization")
    date_quittancement = fields.Selection([('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'),('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),('31', '31')], string="Date de quittancement", help="La date selon laquelle vos quittances seraient datées")
    ref_rental = fields.Char(string="Identifiant", help="Identifiant de la rental")
    start_rent_date = fields.Date(string="start rented date", required=True)
    end_rent_date = fields.Date(string="end of the lease", required=True)
    payment = fields.Selection([('monthly', 'Monthly'),('bimonthly', 'Bimonthly'),('quarterly', 'Quarterly'),('half-yearly', 'Half-yearly'),('annuel', 'Annuel'),('inclusive', 'Inclusive')], string="payments", required=True)
    rent_without_charges = fields.Float(string="rent without charges", related='estate_rented.charges_rent', default=0.0, digits=dp.get_precision('rent without charges'), required=True)
    charges_rent = fields.Float(string="Charges", default=0.0, digits=dp.get_precision('Charges'))
    rent_with_charges = fields.Float(string="rent charges comprises", default=0.0, digits=dp.get_precision('rent charges comprises'), readonly=True, compute='_rent_charges')
    late_fees= fields.Float(string='Late Fees (%)', default=0.0, digits=dp.get_precision('Frais de retard (%)'))
    other_payment = fields.Float(string='other payments', digits=dp.get_precision('other payments'))
    description_other_payment = fields.Text(string="other payments : Description")
    registering_payment = fields.One2many('lb.payment', 'payment_id', string="payments")
    special_condition = fields.Text(string="Conditions")
    remaining_balance = fields.Float(string="Remaining Balance", default=0.0, digits=dp.get_precision('Remaining Balance'))
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('lb.rental'), index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")
    partner_a_jour = fields.Selection([('yes', 'yes'),('no', 'No')], string="Le partner est-il à jour ?")

    _sql_constraints = [     
    ('reference_rental_unique',
    'UNIQUE(ref_rental)',
    "Referance Must be Unique"),
    ]

    _sql_constraints = [     
    ('leasing_estate_unique',
    'UNIQUE(estate_rented)',
    "Rental estate leasing Unique"),
    ]

	
            # Calcul du rent
    @api.multi
    def _rent_charges(self):
        for r in self:
            r.rent_with_charges = r.rent_without_charges + r.charges_rent

            # Statut rental
    @api.model
    def update_statut(self):
        for r in self:
            if r.start_rent_date and r.end_rent_date:
                if r.start_rent_date <= fields.Date.to_string(date.today()) and r.end_rent_date >= fields.Date.to_string(date.today()):
                    r.rental_status = 'active'
                else:
                    r.rental_status = 'inactive'

            # Calcul de la devise
    @api.multi
    def _compute_currency_id(self):
        try:
            main_company = self.sudo().env.ref('base.main_company')
        except ValueError:
            main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id
			
            # Contrat attaché

    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for estate in self:
            estate.doc_count = Attachment.search_count([('res_model', '=', 'lb.rental'), ('res_id', '=', estate.id)])

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [('res_model', '=', 'lb.rental'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        clik to add rental contract</p><p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

    @api.constrains('start_rent_date', 'end_rent_date')
    def _check_start_end_rent_date(self):
        for r in self:
            if r.start_rent_date > r.end_rent_date:
                raise exceptions.ValidationError("contract end date must biger thane then contract start date")


class payment(models.Model):
    _name = 'lb.payment'
    _rec_name = 'payment_id'

    payment_id = fields.Many2one('lb.rental', ondelete='cascade', string="rental")
    partner_id = fields.Many2one(related='payment_id.partner', string="partner", store=True)
    rental_status_id = fields.Selection(related='payment_id.rental_status', string="Statut de la rental")
    end_rent_date_id = fields.Date(related='payment_id.end_rent_date', string="end of the lease")
    date_payment = fields.Date(string="Date de payment", required=True)
    start_period_date = fields.Date(string="period paid : start", required=True)
    end_period_date = fields.Date(string="period paid : end", required=True)
    paid_amount = fields.Float(string="Paid_amount", default=0.0, digits=dp.get_precision('Montant Payé'), required=True)
    commentaire_payment = fields.Text(string="Commentaire")
    objet_payment = fields.Selection([('avance', 'Avance'),('rent', 'rent du mois'),('pénalité', 'Pénalités'),('other payments', 'others payments')], string="Objet du payment")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('lb.rental'), index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')

            # Calcul de la devise
    @api.multi
    def _compute_currency_id(self):
        try:
            main_company = self.sudo().env.ref('base.main_company')
        except ValueError:
            main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id

