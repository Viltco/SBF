

from odoo import models, fields, api
from odoo.exceptions import UserError
import math

class MaterialPurchaseRequisitionInh(models.Model):
    _inherit = 'material.purchase.requisition'

    requisition_product_lines = fields.One2many('requisition.product.lines', 'req_product_id')
    vendor_id = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product')
    qty = fields.Float('Quantity')
    requisition_type = fields.Selection(selection=[
        ('internal', 'Internal Picking'),
        ('purchase', 'Purchase Order'),],string='Requisition Action')
    is_components_added = fields.Boolean(copy=False)

    def action_add_merged_lines(self):
        product_list = []
        for line in self.requisition_line_ids:
            if not any(d['product_id'] == line.product_id.id for d in product_list):
                product_list.append({
                    'product_id': line.product_id.id,
                    'qty_in_cm': line.qty,
                    'qty': line.qty,
                    'uom_id': line.product_id.uom_id.id,
                })
            else:
                for rec in product_list:
                    if rec['product_id'] == line.product_id.id:
                        rec['qty'] = rec['qty'] + line.qty
                        rec['qty_in_cm'] = rec['qty_in_cm'] + line.qty
        new_list = []
        for res in product_list:
            new_list.append((0, 0, res))
        self.requisition_product_lines = new_list
        for j in self.requisition_product_lines:
            j.qty = math.ceil(round(j.qty/j.product_id.uom_po_id.factor_inv, 2))

    def action_add_components(self):
        product_list = []
        # bom_list = []
        # for line in self.requisition_line_ids:
        # line = self.product_id
        # if line.requisition_type == 'purchase':
        bom = self.env['mrp.bom'].search([('product_id', '=', self.product_id.id)])
        if bom:
            for line_two in bom.bom_line_ids:
                bom_two = self.env['mrp.bom'].search([('product_id', '=', line_two.product_id.id)])
                if bom_two:
                    for line_three in bom_two.bom_line_ids:
                        bom_three = self.env['mrp.bom'].search([('product_id', '=', line_three.product_id.id)])
                        if bom_three:
                            for line_four in bom_three.bom_line_ids:
                                bom_four = self.env['mrp.bom'].search(
                                    [('product_id', '=', line_four.product_id.id)])
                                if bom_four:
                                    for line_five in bom_four.bom_line_ids:
                                        if line_five.product_id.type == 'product':
                                            product_list.append((0, 0, {'requisition_type': self.requisition_type,
                                                                        'product_id': line_five.product_id.id,
                                                                        'description': line_five.product_id.name,
                                                                        'qty': line_five.product_qty * self.qty,
                                                                        'uom': line_five.product_uom_id.id}))
                                else:
                                    if line_four.product_id.type == 'product':
                                        product_list.append((0, 0, {
                                            'requisition_type': self.requisition_type,
                                            'product_id': line_four.product_id.id,
                                            'description': line_four.product_id.name,
                                            'qty': line_four.product_qty * self.qty,
                                            'uom': line_four.product_uom_id.id}))
                        else:
                            if line_three.product_id.type == 'product':
                                product_list.append((0, 0, {'requisition_type': self.requisition_type,
                                                            'product_id': line_three.product_id.id,
                                                            'description': line_three.product_id.name,
                                                            'qty': line_three.product_qty * self.qty,
                                                            'uom': line_three.product_uom_id.id}))
                else:
                    if line_two.product_id.type == 'product':
                        product_list.append((0, 0,
                                             {
                                                 'requisition_type': self.requisition_type,
                                                 'product_id': line_two.product_id.id,
                                                 'description': line_two.product_id.name,
                                                 'qty': line_two.product_qty * self.qty,
                                                 'uom': line_two.product_uom_id.id}))
            self.requisition_line_ids = product_list
            self.action_add_merged_lines()
        self.is_components_added = True

    def action_add_vendors(self):
        if self.vendor_id:
            for line in self.requisition_line_ids:
                line.partner_id = [self.vendor_id.id]
        else:
            raise UserError('Please Select Vendor.')

    def manager_approve(self):
        if self.requisition_type:
            for line in self.requisition_line_ids:
                if line.requisition_type != 'False':
                    line.requisition_type = self.requisition_type
        return super(MaterialPurchaseRequisitionInh, self).manager_approve()

    # def action_get_components(self):
    #     product_list = []
    #     bom_list = []
    #     for line in self.requisition_line_ids:
    #         if line.requisition_type == 'purchase':
    #             bom = self.env['mrp.bom'].search([('product_id', '=', line.product_id.id)])
    #             if bom:
    #                 bom_list.append((0, 0, {'product_id': line.product_id.id, 'qty': line.qty, 'uom_id': line.uom.id}))
    #                 for line_two in bom.bom_line_ids:
    #                     bom_two = self.env['mrp.bom'].search([('product_id', '=', line_two.product_id.id)])
    #                     if bom_two:
    #                         for line_three in bom_two.bom_line_ids:
    #                             bom_three = self.env['mrp.bom'].search([('product_id', '=', line_three.product_id.id)])
    #                             if bom_three:
    #                                 for line_four in bom_three.bom_line_ids:
    #                                     bom_four = self.env['mrp.bom'].search(
    #                                         [('product_id', '=', line_four.product_id.id)])
    #                                     if bom_four:
    #                                         for line_five in bom_four.bom_line_ids:
    #                                             product_list.append((0, 0, {'requisition_type': 'purchase', 'product_id': line_five.product_id.id, 'description': line_five.product_id.name , 'qty': line_five.product_qty* line.qty,  'uom': line_five.product_uom_id.id}))
    #                                     else:
    #                                         product_list.append((0, 0, {'requisition_type': 'purchase', 'product_id': line_four.product_id.id, 'description': line_four.product_id.name , 'qty': line_four.product_qty* line.qty,  'uom': line_four.product_uom_id.id}))
    #                             else:
    #                                 product_list.append((0, 0, {'requisition_type': 'purchase', 'product_id': line_three.product_id.id,'description': line_three.product_id.name , 'qty': line_three.product_qty* line.qty,  'uom': line_three.product_uom_id.id}))
    #                     else:
    #                         product_list.append((0, 0, {'requisition_type': 'purchase', 'product_id': line_two.product_id.id,'description': line_two.product_id.name , 'qty': line_two.product_qty* line.qty,  'uom': line_two.product_uom_id.id}))
    #                 line.unlink()
    #     self.requisition_line_ids = product_list
    #     self.requisition_product_lines = bom_list


class MaterialPurchaseRequisitionLines(models.Model):
    _name = 'requisition.product.lines'

    req_product_id = fields.Many2one('material.purchase.requisition')
    product_id = fields.Many2one('product.product')
    qty = fields.Float('Quantity')
    uom_id = fields.Many2one('uom.uom')
    qty_in_cm = fields.Float('Qty in CM')