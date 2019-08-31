# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression

class city(models.Model):
    _name = 'lb.city'
    _rec_name = 'name'

    name = fields.Char(string="City")


class district(models.Model):
    _name = 'lb.district'
    _rec_name = 'district_name'

    district_name = fields.Char(string="District")
    city_partner = fields.Many2one('lb.city')

