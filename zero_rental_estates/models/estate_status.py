# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from datetime import datetime
from odoo.exceptions import UserError, AccessError
from odoo.tools import float_compare, pycompat
from odoo.addons import decimal_precision as dp


class Estate_status(models.Model):
    _name = 'lb.estate_status'
    _rec_name = 'ref_estate_status'

    estate_status_type = fields.Selection([('entry', 'Estate status d\'entry'),('exit', 'Estate status of exit')], string="Type", required=True)
    date_estate_status = fields.Date(string="Date", required=True)
    ref_estate_status = fields.Char(string="Identifier", help="Identifier unique of estate status")
    notes = fields.Text(string="Notes")
    rental = fields.Many2one('lb.rental', ondelete='cascade', string="Rental related", required=True)
    registering_estate_status = fields.One2many('lb.registering_estate_status', 'estate_status_id', string="Estate status")
    estate_status_entry_related = fields.Many2one('lb.estate_status', string="Estate status of entry relation", domain=[('estate_status_type', '=', 'entry')])
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")	

    _sql_constraints = [     
    ('reference_unique',
    'UNIQUE(ref_estate_status)',
    "The reference of estate atstus muste be unique"),
    ]
            # 2 functions for the attached image

    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for estate in self:
            estate.doc_count = Attachment.search_count([('res_model', '=', 'lb.estate_status'), ('res_id', '=', estate.id)])

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [('res_model', '=', 'lb.estate_status'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Click create (not import) to add the images.</p><p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }


class Registering_Estate_status(models.Model):
    _name = 'lb.registering_estate_status'

    estate_status_id = fields.Many2one('lb.estate_status', ondelete='cascade', string="Estate status")
    name_piece = fields.Char(string="Name of the unit", required=True)
    Estate = fields.Selection([('non verified.', 'Non verified'),('new', 'New'),('good estate', 'Good estate'),('medium estate','medium Estate'),('bad estate', 'Bad estate')], string="Estate")
    comment = fields.Text(string="Comment")

	
