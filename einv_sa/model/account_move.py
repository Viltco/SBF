# -*- coding: utf-8 -*-


from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
# from translate import Translator
# import arabic_reshaper
# from bidi.algorithm import get_display

class AccountMovennInh(models.Model):
    _inherit = 'account.edi.document'

    def action_export_xml(self):
        pass

class AccountMove(models.Model):
    _name = "account.move"
    _inherit = "account.move"

    einv_amount_sale_total = fields.Monetary(string="Amount sale total", compute="_compute_total", store='True', help="")
    einv_amount_discount_total = fields.Monetary(string="Amount discount total", compute="_compute_total", store='True', help="")
    einv_amount_tax_total = fields.Monetary(string="Amount tax total", compute="_compute_total", store='True', help="")
    time_confirm = fields.Char(string="Confirm Time")

    def action_post(self):
        super(AccountMove, self).action_post()
        t = datetime.now().strftime("%H:%M:%S")
        self.time_confirm = str(t)

    def get_amount_in_words(self):
        print('abc')
        amount_in_words = self.currency_id.amount_to_text(self.amount_total)
        amount_in_words = amount_in_words +" "+ "Only"
        print(amount_in_words)
        return amount_in_words



    # def formatArabicSentences(sentences):
    #     formatedSentences = arabic_reshaper.reshape(sentences)
    #     return get_display(formatedSentences)

    # def formatArabicSentences(self):
    #     amount_in_words = self.currency_id.amount_to_text(self.amount_total)
    #     amount_in_words = amount_in_words + " " + "Only"
    #     translator = Translator(from_lang="english", to_lang="arabic")
    #     translation = translator.translate(amount_in_words)
    #     return translation



    # amount_invoiced = fields.Float(string="Amount tax total", help="")
    # qrcode = fields.Char(string="QR", help="")

    @api.depends('invoice_line_ids', 'amount_total')
    def _compute_total(self):
        for r in self:
            r.einv_amount_sale_total = r.amount_untaxed + sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_discount_total = sum(line.einv_amount_discount for line in r.invoice_line_ids)
            r.einv_amount_tax_total = sum(line.einv_amount_tax for line in r.invoice_line_ids)

    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()

        # do the things here
        return res




class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"
    einv_amount_discount = fields.Monetary(string="Amount discount", compute="_compute_amount_discount", store='True', help="")
    einv_amount_tax = fields.Monetary(string="Amount tax", compute="_compute_amount_tax", store='True', help="")

    @api.depends('discount', 'quantity', 'price_unit')
    def _compute_amount_discount(self):
        for r in self:
            r.einv_amount_discount = r.quantity * r.price_unit * (r.discount / 100)

    @api.depends('tax_ids', 'discount', 'quantity', 'price_unit')
    def _compute_amount_tax(self):
        for r in self:
            r.einv_amount_tax = sum(r.price_subtotal * (tax.amount / 100) for tax in r.tax_ids)
