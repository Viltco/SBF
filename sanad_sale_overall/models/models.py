# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


# class SaleInherit(models.Model):
#     _inherit = 'sale.order'
#
#     def write(self, vals):
#         if vals.get('order_line'):
#             self.message_post(body=_('updated: %s') % vals.get('order_line'))
#         res = super(SaleInherit, self).write(vals)
#         return res

class SaleLineInherit(models.Model):
    _inherit = 'sale.order.line'

    # def _update_line_quantity(self, values):
    #     orders = self.mapped('order_id')
    #     for order in orders:
    #         order_lines = self.filtered(lambda x: x.order_id == order)
    #         msg = "<b>" + _("The ordered quantity has been updated.") + "</b><ul>"
    #         for line in order_lines:
    #             msg += "<li> %s: <br/>" % line.product_id.display_name
    #             msg += _(
    #                 "Ordered Quantity: %(old_qty)s -> %(new_qty)s",
    #                 old_qty=line.product_uom_qty,
    #                 new_qty=values["product_uom_qty"]
    #             ) + "<br/>"
    #             if line.product_id.type in ('consu', 'product'):
    #                 msg += _("Delivered Quantity: %s", line.qty_delivered) + "<br/>"
    #             msg += _("Invoiced Quantity: %s", line.qty_invoiced) + "<br/>"
    #         msg += "</ul>"
    #         order.message_post(body=msg)

    def _update_line_price(self, values):
        orders = self.mapped('order_id')
        for order in orders:
            order_lines = self.filtered(lambda x: x.order_id == order)
            msg = "<b>" + _("The price unit has been updated.") + "</b><ul>"
            for line in order_lines:
                msg += "<li> %s: <br/>" % line.product_id.display_name
                msg += _(
                    "Price Unit: %(old_qty)s -> %(new_qty)s",
                    old_qty=line.price_unit,
                    new_qty=values["price_unit"]
                ) + "<br/>"
                # if line.product_id.type in ('consu', 'product'):
                #     msg += _("Delivered Quantity: %s", line.qty_delivered) + "<br/>"
                # msg += _("Invoiced Quantity: %s", line.qty_invoiced) + "<br/>"
            msg += "</ul>"
            order.message_post(body=msg)

    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(_("You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type."))

        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            self.filtered(
                lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) != 0)._update_line_quantity(values)

        if 'price_unit' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            self.filtered(
                # lambda r: r.state == 'sale' and float_compare(r.product_uom_qty, values['product_uom_qty'], precision_digits=precision) != 0)._update_line_quantity(values)
                lambda r: r.state == 'sale' and float_compare(r.price_unit, values['price_unit'], precision_digits=precision) != 0)._update_line_price(values)

        # Prevent writing on a locked SO.
        protected_fields = self._get_protected_fields()
        if 'done' in self.mapped('order_id.state') and any(f in values.keys() for f in protected_fields):
            protected_fields_modified = list(set(protected_fields) & set(values.keys()))
            fields = self.env['ir.model.fields'].search([
                ('name', 'in', protected_fields_modified), ('model', '=', self._name)
            ])
            raise UserError(
                _('It is forbidden to modify the following fields in a locked order:\n%s')
                % '\n'.join(fields.mapped('field_description'))
            )

        result = super(SaleLineInherit, self).write(values)
        return result


# class PurchaseInherit(models.Model):
#     _inherit = 'purchase.order'
#
#     def write(self, vals):
#         if vals.get('order_line'):
#             result = vals.get('order_line')
#             print(result)
#             if result[0][2]['product_qty']:
#                 qty = result[0][2]['product_qty']
#                 self.message_post(body=_('Updated: New Quantity ' + str(qty)))
#             if result[0][2]['price_unit']:
#                 price = result[0][2]['price_unit']
#                 self.message_post(body=_('Updated: New Price ' + str(price)))
#             # self.message_post(body=_('updated: %s') % vals.get('order_line'))
#             # self.message_post(body=_('Updated: New Price ' + str(price) + ' & New Quantity '+str(qty)))
#         res = super(PurchaseInherit, self).write(vals)
#         return res


class PurchaseLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                _("You cannot change the type of a purchase order line. Instead you should delete the current line and create a new line of the proper type."))

        if 'product_qty' in values:
            for line in self:
                line.order_id.message_post_with_view('purchase.track_po_line_template',
                                                     values={'line': line, 'product_qty': values['product_qty']},
                                                     subtype_id=self.env.ref('mail.mt_note').id)
        if 'price_unit' in values:
            for line in self:
                line._track_price_unit(values['price_unit'])
                # line.order_id.message_post_with_view(values={'line': line,  'price_unit': values['price_unit']},
                #                                      subtype_id=self.env.ref('mail.mt_note').id)

        if 'qty_received' in values:
            for line in self:
                line._track_qty_received(values['qty_received'])
        return super(PurchaseLineInherit, self).write(values)


    def _track_price_unit(self, new_price):
        self.ensure_one()
        self.order_id.message_post_with_view(
            'sanad_sale_overall.track_po_line_price_unit_template',
            values={'line': self, 'price_unit': new_price},
            subtype_id=self.env.ref('mail.mt_note').id
        )


