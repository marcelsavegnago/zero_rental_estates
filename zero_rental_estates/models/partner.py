# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp
    

class Partner(models.Model):
    _inherit = 'res.partner'

    identity_type = fields.Selection([('NCI','National card d\'identity'),('Visit_Card','Visa Cart'),('passport','Passport')],string='Type of identity d\'identity')
    identity_id = fields.Char(string='Number if identity d\'identity')
    city = fields.Char()
    type = fields.Selection([('contact','Contact')], string='Address Type', help="Used to select automatically the right address according to the context in sales and purchases documents.")
    city = fields.Char()
    contact_registeration = fields.One2many('lb.contact','contact_id', string="Contact")

class Contact(models.Model):
    _name = 'lb.contact'

    contact_id = fields.Many2one('res.partner', ondelete='cascade', string="Contact")
    contact_name = fields.Char(string="Contact Name", required=True)
    contact_phone = fields.Char(string="Telephone", required=True)
    contact_email = fields.Char(string="E-mail")
    contact_notes = fields.Text(string="Notes")

