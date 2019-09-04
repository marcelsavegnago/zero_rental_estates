# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp


class Tenant(models.Model):
    _inherit = 'res.partner'

    identite_type = fields.Selection([('id', 'Create national d\'identite'),('carte_visit', 'create the visit'),('passport', 'Passport')],string='Type of the d\'identite')
    identite_no = fields.Char(string='Nomber of d\'identite')
    city = fields.Char()
    type = fields.Selection([('contact', 'Contact')], string='Address Type', help="Used to select automatically the right address according to the context in sales and purchases documents.")
    city = fields.Char()
    registering_contact = fields.One2many('lb.contact', 'contact_id', string="Contact")

class Contact(models.Model):
    _name = 'lb.contact'

    contact_id = fields.Many2one('res.partner', ondelete='cascade', string="Contact")
    contact_name = fields.Char(string="Name of Contact", required=True)
    contact_phone = fields.Char(string="Telephone", required=True)
    contact_email = fields.Char(string="E-mail")
    contact_notes = fields.Text(string="Notes")

