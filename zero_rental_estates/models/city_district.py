# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.tools import float_compare, pycompat
from odoo.exceptions import ValidationError
from odoo.osv import expression



class City(models.Model):
    _name = 'lb.city'
    _rec_name = 'name'

    name = fields.Char(string="City")


class District(models.Model):
    _name = 'lb.district'
    _rec_name = 'name_district'

    name_district = fields.Char(string="District")
    city_partner = fields.Many2one('lb.city')

