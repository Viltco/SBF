

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import math
from datetime import datetime


class PurchaseRequisitionInh(models.Model):
    _inherit = 'purchase.requisition'

    requisition_id = fields.Many2one('material.purchase.requisition')
    is_created_po = fields.Boolean('')
    # purchase_count = fields.Integer(compute='_compute_po')
    #
    # def _compute_po(self):
    #     count = self.env['purchase.order'].search_count([('requisition_id', '=', self.id)])
    #     self.purchase_count = count

    def action_view_po(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'res_model': 'purchase.order',
            'domain': [('requisition_id', '=', self.id)],
            'view_mode': 'tree,form',
        }

    def request_stock(self):
        # stock_obj = self.env['stock.picking']
        # move_obj = self.env['stock.move']
        # internal_obj = self.env['stock.picking.type'].search([('code','=', 'internal')], limit=1)
        purchase_obj = self.env['purchase.order']
        purchase_line_obj = self.env['purchase.order.line']
        #         if not internal_obj:
        #             raise UserError(_('Please Specified Internal Picking Type.'))
        pur = -1
        for rec in self.requisition_id:
            if not rec.requisition_line_ids:
                raise Warning(_('Please create some requisition lines.'))
            # if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
            #     if not rec.location_id.id:
            #         raise Warning(_('Select Source location under the picking details.'))
            #     if not rec.custom_picking_type_id.id:
            #         raise Warning(_('Select Picking Type under the picking details.'))
            #     if not rec.dest_location_id:
            #         raise Warning(_('Select Destination location under the picking details.'))
            #     #                 if not rec.employee_id.dest_location_id.id or not rec.employee_id.department_id.dest_location_id.id:
            #     #                     raise Warning(_('Select Destination location under the picking details.'))
            #     picking_vals = {
            #         'partner_id': rec.employee_id.sudo().address_home_id.id,
            #         # 'min_date' : fields.Date.today(),
            #         'location_id': rec.location_id.id,
            #         'location_dest_id': rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
            #         'picking_type_id': rec.custom_picking_type_id.id,
            #         'note': rec.reason,
            #         'custom_requisition_id': rec.id,
            #         'origin': rec.name,
            #         'company_id': rec.company_id.id,
            #     }
            #     stock_id = stock_obj.sudo().create(picking_vals)
            #     delivery_vals = {
            #         'delivery_picking_id': stock_id.id,
            #     }
            #     rec.write(delivery_vals)
            po_dict = {}
            for line in rec.requisition_line_ids:
                # if line.requisition_type == 'internal':
                #     pick_vals = rec._prepare_pick_vals(line, stock_id)
                #     move_id = move_obj.sudo().create(pick_vals)
                # else:
                if line.requisition_type == 'purchase':  # 10/12/2019
                    if not line.partner_id:
                        raise Warning(
                            _('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
                    for partner in line.partner_id:
                        if partner not in po_dict:
                            po_vals = {
                                'partner_id': partner.id,
                                'currency_id': rec.env.user.company_id.currency_id.id,
                                'date_order': fields.Date.today(),
                                #                                'company_id':rec.env.user.company_id.id,
                                'company_id': rec.company_id.id,
                                'custom_requisition_id': rec.id,
                                'origin': self.name,
                                'requisition_id': self.id,
                                'user_id': self.env.user.id,
                            }
                            purchase_order = purchase_obj.create(po_vals)
                            # pur = purchase_order
                            po_dict.update({partner: purchase_order})
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            #                            {
                            #                                     'product_id': line.product_id.id,
                            #                                     'name':line.product_id.name,
                            #                                     'product_qty': line.qty,
                            #                                     'product_uom': line.uom.id,
                            #                                     'date_planned': fields.Date.today(),
                            #                                     'price_unit': line.product_id.lst_price,
                            #                                     'order_id': purchase_order.id,
                            #                                     'account_analytic_id': rec.analytic_account_id.id,
                            #                            }
                            purchase_line_obj.sudo().create(po_line_vals)
                            pur = purchase_line_obj
                        else:
                            purchase_order = po_dict.get(partner)
                            pur = purchase_order
                            po_line_vals = rec._prepare_po_line(line, purchase_order)
                            #                            po_line_vals =  {
                            #                                 'product_id': line.product_id.id,
                            #                                 'name':line.product_id.name,
                            #                                 'product_qty': line.qty,
                            #                                 'product_uom': line.uom.id,
                            #                                 'date_planned': fields.Date.today(),
                            #                                 'price_unit': line.product_id.lst_price,
                            #                                 'order_id': purchase_order.id,
                            #                                 'account_analytic_id': rec.analytic_account_id.id,
                            #
                            #                            }
                            check = False
                            for p_line in purchase_order.order_line:
                                if p_line.product_id.id == line.product_id.id:
                                    p_line.product_qty = (line.qty/line.product_id.uom_po_id.factor_inv) + p_line.product_qty
                                    check = True
                            if not check:
                                purchase_line_obj.sudo().create(po_line_vals)
            # if rec.requi_act_ip_po == True:
            #     rec.state = 'po_pick'
            # else:
            #     rec.state = 'stock'
        self.is_created_po = True
        if pur != -1:
            if pur:
                for u_rec in pur.order_line:
                    u_rec.product_qty = math.ceil(round(u_rec.product_qty, 2))


class MaterialPurchaseRequisitionInh(models.Model):
    _inherit = 'material.purchase.requisition'

    requisition_product_lines = fields.One2many('requisition.product.lines', 'req_product_id')
    vendor_id = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product')
    qty = fields.Float('Quantity')
    requisition_type = fields.Selection(selection=[
        ('internal', 'Internal Picking'),
        ('purchase', 'Purchase Order')], string='Requisition Action')
    is_components_added = fields.Boolean(copy=False)
    agreement_count = fields.Integer(compute='compute_agreement_count')

    def compute_agreement_count(self):
        count = self.env['purchase.requisition'].search_count([('requisition_id', '=', self.id)])
        self.agreement_count = count

    def request_stock(self):
        stock_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        # internal_obj = self.env['stock.picking.type'].search([('code','=', 'internal')], limit=1)
        # purchase_obj = self.env['purchase.order']
        # purchase_line_obj = self.env['purchase.order.line']
        #         if not internal_obj:
        #             raise UserError(_('Please Specified Internal Picking Type.'))
        # pur = -1
        self.action_create_agreement()
        for rec in self:
            if not rec.requisition_line_ids:
                raise UserError(_('Please create some requisition lines.'))
            if any(line.requisition_type == 'internal' for line in rec.requisition_line_ids):
                if not rec.location_id.id:
                    raise UserError(_('Select Source location under the picking details.'))
                if not rec.custom_picking_type_id.id:
                    raise UserError(_('Select Picking Type under the picking details.'))
                if not rec.dest_location_id:
                    raise UserError(_('Select Destination location under the picking details.'))
                #                 if not rec.employee_id.dest_location_id.id or not rec.employee_id.department_id.dest_location_id.id:
                #                     raise Warning(_('Select Destination location under the picking details.'))
                picking_vals = {
                    'partner_id': rec.employee_id.sudo().address_home_id.id,
                    # 'min_date' : fields.Date.today(),
                    'location_id': rec.location_id.id,
                    'location_dest_id': rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                    'picking_type_id': rec.custom_picking_type_id.id,
                    'note': rec.reason,
                    'custom_requisition_id': rec.id,
                    'origin': rec.name,
                    'company_id': rec.company_id.id,
                }
                stock_id = stock_obj.sudo().create(picking_vals)
                delivery_vals = {
                    'delivery_picking_id': stock_id.id,
                }
                rec.write(delivery_vals)

            po_dict = {}
            for line in rec.requisition_line_ids:
                if line.requisition_type == 'internal':
                    pick_vals = rec._prepare_pick_vals(line, stock_id)
                    move_id = move_obj.sudo().create(pick_vals)
                # else:
                # if line.requisition_type == 'purchase':  # 10/12/2019
                #     if not line.partner_id:
                #         raise Warning(
                #             _('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
                #     for partner in line.partner_id:
                #         if partner not in po_dict:
                #             po_vals = {
                #                 'partner_id': partner.id,
                #                 'currency_id': rec.env.user.company_id.currency_id.id,
                #                 'date_order': fields.Date.today(),
                #                 #                                'company_id':rec.env.user.company_id.id,
                #                 'company_id': rec.company_id.id,
                #                 'custom_requisition_id': rec.id,
                #                 'origin': rec.name,
                #                 'user_id': self.env.user.id,
                #             }
                #             purchase_order = purchase_obj.create(po_vals)
                #             # pur = purchase_order
                #             po_dict.update({partner: purchase_order})
                #             po_line_vals = rec._prepare_po_line(line, purchase_order)
                #             #                            {
                #             #                                     'product_id': line.product_id.id,
                #             #                                     'name':line.product_id.name,
                #             #                                     'product_qty': line.qty,
                #             #                                     'product_uom': line.uom.id,
                #             #                                     'date_planned': fields.Date.today(),
                #             #                                     'price_unit': line.product_id.lst_price,
                #             #                                     'order_id': purchase_order.id,
                #             #                                     'account_analytic_id': rec.analytic_account_id.id,
                #             #                            }
                #             purchase_line_obj.sudo().create(po_line_vals)
                #             pur = purchase_line_obj
                #         else:
                #             purchase_order = po_dict.get(partner)
                #             pur = purchase_order
                #             po_line_vals = rec._prepare_po_line(line, purchase_order)
                #             #                            po_line_vals =  {
                #             #                                 'product_id': line.product_id.id,
                #             #                                 'name':line.product_id.name,
                #             #                                 'product_qty': line.qty,
                #             #                                 'product_uom': line.uom.id,
                #             #                                 'date_planned': fields.Date.today(),
                #             #                                 'price_unit': line.product_id.lst_price,
                #             #                                 'order_id': purchase_order.id,
                #             #                                 'account_analytic_id': rec.analytic_account_id.id,
                #             #
                #             #                            }
                #             check = False
                #             for p_line in purchase_order.order_line:
                #                 if p_line.product_id.id == line.product_id.id:
                #                     p_line.product_qty = (line.qty/line.product_id.uom_po_id.factor_inv) + p_line.product_qty
                #                     check = True
                #             if not check:
                #                 purchase_line_obj.sudo().create(po_line_vals)
            if rec.requi_act_ip_po == True:
                rec.state = 'po_pick'
            else:
                rec.state = 'stock'
        # if pur != -1:
        #     if pur:
        #         for u_rec in pur.order_line:
        #             u_rec.product_qty = math.ceil(round(u_rec.product_qty, 2))

    def action_create_agreement(self):
        product_list = []
        for line in self.requisition_line_ids:
            if line.requisition_type == 'purchase':
                if not line.partner_id:
                    raise UserError('Plz Add vendor.')
                if not any(d['product_id'] == line.product_id.id for d in product_list):
                    product_list.append({
                        'product_id': line.product_id.id,
                        'product_qty': line.qty,
                        'price_unit': line.product_id.lst_price,
                        # 'qty': line.qty,
                        'product_uom_id': line.product_id.uom_po_id.id,
                    })
                else:
                    for rec in product_list:
                        if rec['product_id'] == line.product_id.id:
                            rec['product_qty'] = rec['product_qty'] + line.qty
                            # rec['qty_in_cm'] = rec['qty_in_cm'] + line.qty
        new_list = []
        for res in product_list:
            new_list.append((0, 0, res))
        vals = {
            'user_id': self.env.user.id,
            # 'invoice_date': datetime.today().date(),
            'line_ids': new_list,
            'state': 'draft',
            'origin': self.name,
            'requisition_id': self.id,
        }
        req = self.env['purchase.requisition'].create(vals)
        for j in req.line_ids:
            j.product_qty = math.ceil(round(j.product_qty / j.product_id.uom_po_id.factor_inv, 2))
        req.action_in_progress()
        req.request_stock()
        # self.requisition_product_lines = new_list


    def action_view_purchase_agreement(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Agreement',
            'res_model': 'purchase.requisition',
            'domain': [('origin', '=', self.name)],
            'view_mode': 'tree,form',
        }

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
                if not line.requisition_type:
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