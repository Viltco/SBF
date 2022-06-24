# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMoveInh(models.Model):
    _inherit = 'stock.move'

    @api.onchange('product_id')
    def onchange_product_idss(self):
        for rec in self:
            if rec.picking_id.state != 'draft' and rec.picking_id.picking_type_id.code == 'incoming':
                raise UserError('You cannot add Product in this state')


# class StockMoveLineInh(models.Model):
#     _inherit = 'stock.move.line'
#
#     @api.onchange('product_id')
#     def onchange_product_id(self):
#         if self.picking_id.state == 'draft' and self.picking_id.picking_type_id.code == 'incoming':
#             raise UserError('You cannot add Product in this Stage')


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('qc_inspection', 'QC Inspection'),
        ('assigned', 'Ready'),
        ('approve', 'Waiting For Approval'),
        ('done', 'Done'),
        ('reject', 'Reject'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    document_1 = fields.Boolean()
    # document_2 = fields.Boolean()
    # document_3 = fields.Boolean()
    is_receipt = fields.Boolean()

    def action_ready(self):
        for rec in self.check_ids:
            if rec.quality_state != 'pass':
                raise UserError('Quality Checks Are not Passed.')
        record = super(StockPickingInh, self).action_assign()
        return record

    def action_qc_confirm(self):
        if self.document_1:
            self.state = 'qc_inspection'
        else:
            raise UserError('Delivery Document should be check to "Confirm""')


class PurchaseOrderLineInh(models.Model):
    _inherit = 'purchase.order.line'

    brand = fields.Char()


class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    warranty = fields.Char('Warranty')
    comparison_lines = fields.One2many('comparison.line', 'order_id')

    def action_add_lines(self):
        for res in self:
            product_list = []
            for rec in res.comparison_lines:
                rec.unlink()
            for line in res.order_line:
                product_list.append((0, 3, {
                    'product_id': line.product_id.id,
                    'brand': line.brand,
                    'product_qty': line.product_qty,
                    'discount': line.discount,
                    'price_unit': line.price_unit,
                    'product_uom': line.product_uom.id,
                    'price_subtotal': line.price_subtotal
                }))
            res.comparison_lines = product_list

    def button_cancel(self):
        record = super(PurchaseOrderInh, self).button_cancel()
        for order in self:
            for picking in order.picking_ids:
                if picking.state == 'done':
                    raise UserError('You cannot cancel this purchase order since partial receipt have been made.')
                if picking.state != 'done':
                    picking.action_cancel()
        return record

    def button_manager(self):
        record = super(PurchaseOrderInh, self).button_manager()
        for order in self:
            for picking in order.picking_ids:
                picking.do_unreserve()
                picking.is_receipt = True
        return record


class ComparisonItemsLine(models.Model):
    _name = 'comparison.line'

    order_id = fields.Many2one('purchase.order')
    product_id = fields.Many2one('product.product')
    product_uom = fields.Many2one('uom.uom')
    product_qty = fields.Float('Quantity')
    price_unit = fields.Float()
    price_subtotal = fields.Float()
    discount = fields.Float()
    brand = fields.Char()
    warranty = fields.Char()
