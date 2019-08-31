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
        country = self.env['res.clessory'].search([('code', '=', 'EG')], limit=1)
        return country

    name = fields.Char(string="name", required=True)
    greeting = fields.Selection([('m.', 'M.'),('mrs', 'Mrs'),('mis', 'Mis')], string="Greeting") 
    email = fields.Char(string="E-mail", required=True)
    telephone = fields.Char(string="phone", required=True)
    rue = fields.Char()
    postal_code = fields.Char(string="Postal Code")
    city = fields.Char(string="city")
    country_id = fields.Many2one('res.country', string='country', default=_get_default_country, ondelete='restrict')
    job_titel = fields.Char(string="Job Titel", help="Professional activity of the lessor")
