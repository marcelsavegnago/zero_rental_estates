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
    _rec_name = 'estate_contract'

    estate_contract = fields.Many2one('lb.estate', ondelete='cascade', string="Estate Contract", required=True)
    tenants = fields.Many2one('res.partner', ondelete='cascade', string="tenant", required=True)
    #statut_rental = fields.Selection([('inactive', 'Inactive'),('active', 'Active')], string="Statut", compute='update_statut', help="Statut de la rental (Active : Rental inprogress)")
    utilization = fields.Selection([('utilization1', 'utilization main tenant'),('utilization2', 'utilization secondery of tenant'),('utilization3', 'utilization professional')], string="utilization")
    receip_date = fields.Selection([('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8'),('9', '9'),('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),('31', '31')], string="Date of receipt", help="The date on which your receipts would be dates")
    ref_rental = fields.Char(string="Identifier", help="Identifier of the rental")
    from_date = fields.Date(string="From Date", required=True)
    to_date = fields.Date(string="To Date", required=True)
    payment = fields.Selection([('monthly', 'Monthly'),('bimonthly', 'Bimonthly'),('quarterly', 'Quarterly'),('half-yearly', 'Half-yearly'),('annuel', 'Annuel'),('included', 'Included')], string="payments", required=True)
    rent_without_charges = fields.Float(string="Rent without charges", related='estate_contract.rental_price', default=0.0, digits=dp.get_precision('Rent without charges'), required=True)
    rent_charges = fields.Float(string="Charges", default=0.0, digits=dp.get_precision('Charges'))
    rent_with_charges = fields.Float(string="Rent inclouded charges", default=0.0, digits=dp.get_precision('rent charges included'), readonly=True, compute='_rent_charges')
    late_fees = fields.Float(string='Late fees (%)', default=0.0, digits=dp.get_precision('Late Fees (%)'))
    other_payment = fields.Float(string='other payments', digits=dp.get_precision('other payments'))
    description_other_payment = fields.Text(string="other payments : Description")
    registering_payment = fields.One2many('lb.payment', 'payment_id', string="payments")
    special_condition = fields.Text(string="Conditions")
    remains_to_pay = fields.Float(string="Reste à payer", default=0.0, digits=dp.get_precision('Remains to pay'))
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('lb.rental'), index=1)
    currency_id = fields.Many2one('res.currency', 'Currency', compute='_compute_currency_id')
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")
    keep_up_to_date = fields.Selection([('yes', 'Yes'),('no', 'No')], string="Is The tenant up to date?")

    _sql_constraints = [     
    ('reference_rental_unique',
    'UNIQUE(ref_rental)',
    "The reference must be unique"),
    ]

    _sql_constraints = [     
    ('renting_estate_unique',
    'UNIQUE(estate_contract)',
    "Ce estate est déjà sous rental"),
    ]

	
            # Calcul du rent
    @api.multi
    def _rent_charges(self):
        for r in self:
            r.rent_with_charges = r.rent_without_charges + r.rent_charges

            # Statut rental
    #@api.model
    #def update_statut(self):
      #  for r in self:
            #if r.from_date and r.to_date:
                #if r.from_date <= fields.Date.to_string(date.today()) and r.to_date >= fields.Date.to_string(date.today()):
                  #  r.statut_rental = 'active'
                #else:
                  #  r.statut_rental = 'inactive'

            # Calculation of the currency
    @api.multi
    def _compute_currency_id(self):
        try:
            main_company = self.sudo().env.ref('base.main_company')
        except ValueError:
            main_company = self.env['res.company'].sudo().search([], limit=1, order="id")
        for template in self:
            template.currency_id = template.company_id.sudo().currency_id.id or main_company.currency_id.id
			
            # related attaché

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
                        Click Create (not import) to add your rental contracts</p><p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

    @api.constrains('from_date', 'to_date')
    def _check_from_to_date(self):
        for r in self:
            if r.from_date > r.to_date:
                raise exceptions.ValidationError("The end of the lease must be greater at the The end of the lease must be greater at the beginning of the lease")


class Payment(models.Model):
    _name = 'lb.payment'
    _rec_name = 'payment_id'

    payment_id = fields.Many2one('lb.rental', ondelete='cascade', string="rental")
    tenant_id = fields.Many2one(related='payment_id.tenants', string="tenant", store=True)
    #statut_rental_id = fields.Selection(related='payment_id.statut_rental', string="Statut of the rental")
    to_date_id = fields.Date(related='payment_id.to_date', string="To Date")
    payment_date = fields.Date(string="Date of payment", required=True)
    from_period_date = fields.Date(string="Paid period :From", required=True)
    to_period_date = fields.Date(string="Paid period : To", required=True)
    paid_amount = fields.Float(string="Paid Amount", default=0.0, digits=dp.get_precision('Paid Amount'), required=True)
    commentment_payment = fields.Text(string="Commentment")
    payment_object = fields.Selection([('advance', 'Advance'),('rent', 'Rent of the month'),('penalty', 'penalties'),('other payments', 'Others payments')], string="payment object")
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

