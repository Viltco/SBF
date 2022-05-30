# -*- coding: utf-8 -*-


from odoo import models, fields


class ManufacturingInh(models.Model):
    _inherit = 'mrp.production'

    qty_produce = fields.Integer(string='To Produce')

    def action_confirm(self):
        res = super(ManufacturingInh, self).action_confirm()
        self.qty_produce = self.product_qty
        return res
