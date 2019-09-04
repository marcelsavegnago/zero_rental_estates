# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp


class Lessor(models.Model):
    _name = 'lb.lessor'
    _rec_name = 'name'

	        # Get default country
    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'EG')], limit=1)
        return country

    name = fields.Char(string="Name", required=True)
    greeting = fields.Selection([('m.', 'M.'),('mrs', 'Mrs'),('ms', 'Ms'),('m. and mrs','M. and Mrs')], string="Greeting") 
    email = fields.Char(string="E-mail", required=True)
    telephone = fields.Char(string="Telephone", required=True)
    street = fields.Char()
    postal_code = fields.Char(string="Code Postal")
    city = fields.Char(string="City")
    country_id = fields.Many2one('res.country', string='Countries', default=_get_default_country, ondelete='restrict')
    title = fields.Char(string="Title", help="Professional activity of the owner")
