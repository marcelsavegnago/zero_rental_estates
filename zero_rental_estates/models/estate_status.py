# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from datetime import datetime
from odoo.exceptions import UserError, AccessError
from odoo.tools import float_compare, pycompat
from odoo.addons import decimal_precision as dp

    

class Estate_status(models.Model):
    _name = 'lb.estate_status'
    _rec_name = 'ref_estate_status'

    estate_status_type = fields.Selection([('entry', 'estate status d\'entry'),('exit', 'estate status exit')], string="Type", required=True)
    estate_status_date = fields.Date(string="Date", required=True)
    ref_estate_status = fields.Char(string="estate code", help="unique code for estate status")
    notes = fields.Text(string="Notes")
    rental = fields.Many2one('lb.rental', ondelete='cascade', string="Related rental", required=True)
    registering_estate_status = fields.One2many('lb.registering_estate_status', 'estate_status_id', string="estate Status")
    estate_status_entry_partner = fields.Many2one('lb.estate_status', string="estate Statusd'entry partner", domain=[('estate_status_type', '=', 'entry')])
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Documents")	

    _sql_constraints = [     
    ('reference_unique',
    'UNIQUE(ref_estate_status)',
    "referance of estate is uniqe"),
    ]
            # 2 functions for the attached image

    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for status in self:
            status.doc_count = Attachment.search_count([('res_model', '=', 'lb.estate_status'), ('res_id', '=', status.id)])

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
                        clik to create (and no import) to add related images to your estate.</p><p>
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }


class Registering_estate_status(models.Model):
    _name = 'lb.registering_estate_status'

    estate_status_id = fields.Many2one('lb.estate_status', ondelete='cascade', string="estate Status")
    estate_name = fields.Char(string="name of The estate", required=True)
    status = fields.Selection([('not verified.', 'Not verified'),('new', 'New'),('good', 'Good'),('medium','Medium'),('bad', 'Bad')],string="Status")
    comment = fields.Text(string="Comment")

	
