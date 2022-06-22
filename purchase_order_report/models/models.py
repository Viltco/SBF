# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class PurchaseOrderReport(models.Model):
    _inherit = 'purchase.order'

    attn = fields.Char('ATTN')
    rev = fields.Integer('REV')
    rev_date = fields.Date('Rev Date')
    # req_ref = fields.Char('REQ REF')
    iso_ref = fields.Char('ISO REF')
    special_instruction = fields.Char('Special Instructions')
    special_terms = fields.Text('Special Terms')
    shipment_mode = fields.Selection([
        ('by_road', 'By Road'),
        ('by_air', 'By Air'),
        ('by_sea', 'By Sea')],
        string='Shipment Mode', default="by_road", tracking=True)

    def button_draft(self):
        self.rev = self.rev + 1
        self.rev_date = datetime.today().date()
        rec = super(PurchaseOrderReport, self).button_draft()
