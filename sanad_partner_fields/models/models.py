# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ResUserInh(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        record = super(ResUserInh, self).create(vals)
        record.partner_type = 'employee'
        return record


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(string='Tax ID', size=15, index=True, tracking=1,help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
    cr_no = fields.Char('CR#', default='', size=10, tracking=1)
    partner_type = fields.Selection([
        ('supplier', 'Supplier'), ('customer', 'Customer'), ('employee', 'Employee')],
        index=True, required=True, tracking=15)
    phone = fields.Char(tracking=1)
    mobile = fields.Char(tracking=1)
    email = fields.Char(tracking=1)

    @api.onchange('cr_no')
    def _check_value(self):
        # print(self.context)
        if self.cr_no:
            if not self.cr_no.isnumeric() or len(self.cr_no) < 10:
                raise UserError('Incorrect CR# format: CR# can be numeric only. Must be 10 digits only.')

    @api.onchange('vat')
    def _check_vat(self):
        if self.vat:
            if not self.vat.isnumeric() or len(self.vat) < 15:
                raise UserError('Incorrect TAX ID format: TAX ID can be numeric only. Must be 15 digits only.')

    @api.onchange('partner_type')
    def onchange_partner_type(self):
        if self.partner_type == 'supplier':
            self.customer_rank = 0
            self.supplier_rank = 1
        if self.partner_type == 'customer':
            self.customer_rank = 1
            self.supplier_rank = 0

    @api.onchange('cr_no')
    def set_upper(self):
        self.cr_no = str(self.cr_no).upper()
        return

    @api.constrains('cr_no')
    def check_code(self):
        if self.cr_no:
            code = self.env['res.partner'].search([('cr_no', '=', self.cr_no)])
            if len(code) > 1:
                raise UserError('CR No Already Exist')