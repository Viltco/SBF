from odoo import models, fields, api


class StockMoveLineInh(models.Model):
    _inherit = 'stock.move.line'

    to_consume_sm = fields.Float('To Consume(Roll)', compute='_compute_consume')

    @api.depends('product_uom_qty', 'qty_done', 'state')
    def _compute_consume(self):
        for rec in self:
            if rec.product_id and rec.picking_id.state != 'done':
                rec.to_consume_sm = rec.product_uom_qty / rec.product_id.uom_po_id.factor_inv
            elif rec.product_id and rec.picking_id.state == 'done':
                rec.to_consume_sm = rec.qty_done / rec.product_id.uom_po_id.factor_inv
            else:
                rec.to_consume_sm = 0


class StockPickingInh(models.Model):
    _inherit = 'stock.move'

    to_consume_sm = fields.Float('To Consume(Roll)', compute='_compute_consume')
    to_reserve_sm = fields.Float('To Reserve(Roll)')
    to_consumed_sm = fields.Float('Consumed(Roll)')

    @api.depends('product_uom_qty', 'forecast_availability', 'quantity_done')
    def _compute_consume(self):
        for rec in self:
            if rec.product_uom_qty:
                rec.to_consume_sm = rec.product_uom_qty/rec.product_id.uom_po_id.factor_inv
                rec.to_reserve_sm = rec.forecast_availability / rec.product_id.uom_po_id.factor_inv
                rec.to_consumed_sm = rec.quantity_done / rec.product_id.uom_po_id.factor_inv
            else:
                rec.to_consume_sm = 0
                rec.to_reserve_sm = 0
                rec.to_consumed_sm = 0


#     mo_count = fields.Integer(default=0, compute='compute_mo')
#     show_create_mo = fields.Boolean()
#
#     def action_assign(self):
#         rec = super(StockPickingInh, self).action_assign()
#         for line in self.move_ids_without_package:
#             if  line.reserved_availability < line.product_uom_qty:
#                 bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'normal')])
#                 if bom:
#                     self.show_create_mo = True
#
#     def compute_mo(self):
#         count = self.env['mrp.production'].search_count([('origin', '=', self.name)])
#         self.mo_count = count
#
#     def action_view_mo(self):
#         return {
#             'name': 'MO',
#             'type': 'ir.actions.act_window',
#             'view_mode': 'tree,form',
#             'res_model': 'mrp.production',
#             'domain': [('origin', '=', self.name)],
#         }
#
#     def create_mo(self):
#         product_list = []
#         bom = self.env['mrp.bom'].search([])
#         for rec in bom:
#             product_list.append(rec.product_id.id)
#
#         for line in self.move_ids_without_package:
#             line_vals = []
#             if line.product_id.id in product_list and line.reserved_availability < line.product_uom_qty:
#                 bom_id = self.env['mrp.bom'].search([('product_id', '=', line.product_id.id)])
#                 print(bom_id)
#                 for bom_line in bom_id.bom_line_ids:
#                     line_vals.append((0, 0, {
#                         'product_id': bom_line.product_id.id,
#                         'name': bom_line.product_id.name,
#                         'location_id': line.location_id.id,
#                         'location_dest_id': line.location_dest_id.id,
#                         'product_uom_qty':  bom_line.product_qty,
#                         'product_uom': bom_line.product_uom_id.id,
#                     }))
#                     line_vals.append(line_vals)
#                 vals = {
#                     'picking_for_id': self.id,
#                     'product_id': line.product_id.id,
#                     'company_id': self.env.user.company_id.id,
#                     'date_planned_start': fields.Date.today(),
#                     'move_raw_ids': line_vals,
#                     'location_dest_id': self.location_id.id,
#                     'origin': self.name,
#                     'product_qty': line.product_uom_qty - line.reserved_availability,
#                     'product_uom_id': line.product_id.uom_id.id,
#                 }
#                 mrp = self.env['mrp.production'].create(vals)
#                 self.show_create_mo = False
