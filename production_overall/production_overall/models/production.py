# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError, UserError


# class MrpConsumptionWarningInh(models.TransientModel):
#     _inherit = 'mrp.consumption.warning'
#
#     def action_confirm(self):
#         # print(self.env.context.get('active_id'))
#         mrp = self.env['mrp.production'].browse([self.env.context.get('active_id')])
#         mrp.action_generate_serial()
#         action_from_do_finish = False
#         if self.env.context.get('from_workorder'):
#             if self.env.context.get('active_model') == 'mrp.workorder':
#                 action_from_do_finish = self.env['mrp.workorder'].browse(self.env.context.get('active_id')).do_finish()
#         action_from_mark_done = self.mrp_production_ids.with_context(skip_consumption=True).button_mark_done()
#         return action_from_do_finish or action_from_mark_done
#
#
# class MrpProductionBackorderInh(models.TransientModel):
#     _inherit = 'mrp.production.backorder'
#
#     def action_backorder(self):
#         mo_ids_to_backorder = self.mrp_production_backorder_line_ids.filtered(lambda l: l.to_backorder).mrp_production_id.ids
#         mrp = self.env['mrp.production'].browse(mo_ids_to_backorder)
#         mrp.action_generate_serial()
#         return self.mrp_production_ids.with_context(skip_backorder=True, mo_ids_to_backorder=mo_ids_to_backorder).button_mark_done()

class ProductTemplateInh(models.Model):
    _inherit = 'product.template'

    is_flexible = fields.Boolean('Restrict Flexible Consumption')
    is_process_b = fields.Boolean('Process B')


class UniqueLot(models.Model):
    _name = 'unique.lot'

    mrp_id = fields.Many2one('mrp.production')
    lot_id = fields.Many2one('stock.production.lot')
    name = fields.Char('Lot No')
    status = fields.Selection([
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
    ], string='Status', default='', ondelete='cascade')
    product_id = fields.Many2one('product.product')


class ProducedQtyLine(models.Model):
    _name = 'produced.qty.line'

    mrp_id = fields.Many2one('mrp.production')
    workcenter_id = fields.Many2one('mrp.workcenter')
    workcenter_machine_id = fields.Many2one('centre.machine')
    employee_id = fields.Many2one('hr.employee')
    name = fields.Char('Operation')
    qty = fields.Float('Produced Quantity')
    start_date = fields.Datetime('Start Date')
    paused_date = fields.Datetime('End Date')


class ReasonLine(models.Model):
    _name = 'reason.line'

    mrp_id = fields.Many2one('mrp.production')
    workcenter_id = fields.Many2one('mrp.workcenter')
    workcenter_machine_id = fields.Many2one('centre.machine')
    employee_id = fields.Many2one('hr.employee')
    name = fields.Char('Operation')
    qty = fields.Float('Produced Quantity')
    start_date = fields.Datetime('Start Date')
    paused_date = fields.Datetime('End Date')
    # reason = fields.Char('Reason')
    reason = fields.Selection([
        ('wrong', 'Wrong Cutting'),
        ('burn', 'Burn'),
        ('hole', 'Hole'),
        ('shortage', 'Shortage of material during welding'),
        ('excess', 'Excess of material during welding'),
    ], string='Reason', default='', ondelete='cascade')


class MrpOrderInh(models.Model):
    _inherit = 'mrp.workorder'

    start_date_custom = fields.Datetime('Date Start')
    lot = fields.Char()
    unique_lots = fields.Many2many('unique.lot')

    def button_finish(self):
        for rec in self:
            pre_order = self.env['mrp.workorder'].search([('id', '=', rec.id-1), ('production_id', '=', rec.production_id.id)])
            if pre_order:
                if pre_order.state != 'done':
                    raise UserError('This workorder is waiting for another operation to get done.')
            # record = super(MrpOrderInh, self).button_finish()
            # for rec in self:
            #     qty = 0
            #     for line in rec.production_id.produced_lines:
            #         if line.name == rec.name and line.workcenter_id.id == rec.workcenter_id.id:
            #             qty = qty + line.qty
            #     res = self.env['produced.qty.line'].create({
            #         'mrp_id': rec.production_id.id,
            #         'name': rec.name,
            #         'workcenter_id': rec.workcenter_id.id,
            #         'workcenter_machine_id': rec.workcenter_machine_id.id,
            #         'employee_id': rec.employee_id.id,
            #         'qty': rec.production_id.qty_producing - qty,
            #         'paused_date': datetime.today(),
            #         'start_date': rec.start_date_custom,
            #     })
            if not self.production_id.product_id.is_process_b:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Done Quantity',
                    'view_id': self.env.ref('production_overall.view_done_wizard_form', False).id,
                    'target': 'new',
                    'res_model': 'done.qty.wizard',
                    'view_mode': 'form',
                }
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Finish Lot',
                    'view_id': self.env.ref('production_overall.view_finish_lot_wizard_form', False).id,
                    'target': 'new',
                    'res_model': 'finish.lot.wizard',
                    'view_mode': 'form',
                }

        # return record

    def button_start(self):
        for rec in self:
            pre_order = self.env['mrp.workorder'].search([('id', '=', rec.id-1), ('production_id', '=', rec.production_id.id)])
            # current_qty = sum(self.env['produced.qty.line'].search([('mrp_id', '=', self.production_id.id), ('workcenter_id','=', self.workcenter_id.id), ('workcenter_machine_id','=' , self.workcenter_machine_id.id)]).mapped('qty'))
            # if pre_order:
            #     pre_qty = sum(self.env['produced.qty.line'].search([('mrp_id', '=', pre_order.production_id.id), ('workcenter_id','=', pre_order.workcenter_id.id), ('workcenter_machine_id','=' , pre_order.workcenter_machine_id.id)]).mapped('qty'))
            #     print('Pre',pre_qty)
            # for res in produced_lines:
                # if res.
            # print('Curr',current_qty)
            # if pre_order:
                # if pre_order.state != 'done':
                #     raise UserError('This workorder is waiting for another operation to get done.')

            current_qty = sum(self.env['produced.qty.line'].search(
                [('mrp_id', '=', rec.production_id.id), ('workcenter_id', '=', rec.workcenter_id.id),
                 ('workcenter_machine_id', '=', rec.workcenter_machine_id.id)]).mapped('qty'))
            pre_qty = 0
            if pre_order:
                pre_qty = sum(self.env['produced.qty.line'].search(
                    [('mrp_id', '=', pre_order.production_id.id), ('workcenter_id', '=', pre_order.workcenter_id.id),
                     ('workcenter_machine_id', '=', pre_order.workcenter_machine_id.id)]).mapped('qty'))
                if pre_qty <= current_qty:
                    raise ValidationError('Produced Quantity can not be greater than Quantity to Produce!!!!!!')

            if not rec.production_id.product_id.is_process_b:
                for line in rec.production_id.move_raw_ids:
                    if line.product_uom_qty != line.reserved_availability and rec.production_id.product_id.is_flexible:
                        raise UserError('Required components are not available to start this work order.')
                record = super(MrpOrderInh, self).button_start()
                rec.start_date_custom = datetime.today()
            else:
                # print(self.unique_lots.mapped('id'))
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Produced Lot',
                    'view_id': self.env.ref('production_overall.view_produced_lot_wizard_form', False).id,
                    'target': 'new',
                    'context': {'default_production_id': rec.production_id.id, 'default_unique_lot_ids': rec.unique_lots.ids},
                    'res_model': 'produced.lot.wizard',
                    'view_mode': 'form',
                }

    def button_pending(self):
        record = super(MrpOrderInh, self).button_pending()
        if not self.production_id.product_id.is_process_b:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Produced Quantity',
                'view_id': self.env.ref('production_overall.view_produced_wizard_form', False).id,
                'target': 'new',
                'res_model': 'produced.qty.wizard',
                'view_mode': 'form',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Done Lot',
                'view_id': self.env.ref('production_overall.view_done_lot_wizard_form', False).id,
                'target': 'new',
                'res_model': 'done.lot.wizard',
                'view_mode': 'form',
            }


class MrpInh(models.Model):
    _inherit = 'mrp.production'

    # picking_for_id = fields.Many2one('stock.picking')
    produced_lines = fields.One2many('produced.qty.line', 'mrp_id')
    lot_lines = fields.One2many('unique.lot', 'mrp_id')
    reason_lines = fields.One2many('reason.line', 'mrp_id')

    # lot_producing_id = fields.Many2many('stock.production.lot')
    transfer_count = fields.Integer(default=0, compute='compute_transfers')
    # child_mo_count = fields.Integer(default=0)
    # is_child_mo_created = fields.Boolean()
    show_create_in = fields.Boolean()

    def _create_notification_done(self):
        for res in self:
            act_type_xmlid = 'mail.mail_activity_data_todo'
            summary = 'MO Done'
            note = 'Manufacturing order no:' + res.name + ' Created.'
            if act_type_xmlid:
                activity_type = self.sudo().env.ref(act_type_xmlid)
            model_id = self.env['ir.model']._get(res._name).id
            users = self.env['res.users'].search([])
            for rec in users:
                if rec.has_group('mrp.group_mrp_manager'):
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary or activity_type.summary,
                        'automated': True,
                        'note': note,
                        'date_deadline': datetime.today(),
                        'res_model_id': model_id,
                        'res_id': res.id,
                        # 'user_id': self.sale_id.user_id.id,
                        'user_id': rec.id ,
                    }
                    activities = self.env['mail.activity'].create(create_vals)

    def button_mark_done(self):
        self._create_notification_done()
        # if self.product_id.tracking in ['lot', 'serial']:
        #     if self.lot_producing_id:
        #         for res in self:
        #             i = 1
        #             src = self.origin
        #             mrp = res
        #             while src != False:
        #                 parent = self.env['mrp.production'].search([('name', '=', src)])
        #                 src = parent.origin
        #                 mrp = parent
        #             for rec in range(0, int(res.qty_producing)):
        #                 if i > 9:
        #                     a =  str(i)
        #                 else:
        #                     a = '0' + str(i)
        #                 record = self.env['unique.lot'].create({
        #                     'name': a + '-' + mrp.name.split('/')[-1],
        #                     'lot_id': res.lot_producing_id.id,
        #                     'mrp_id': res.id})
        #                 i = i + 1
        #         return super(MrpInh, self).button_mark_done()
        #     else:
        #         raise ValidationError('Please Add Lot/Serial Number.')
        # else:
        for rec in self.check_ids:
            if rec.quality_state != 'pass':
                raise UserError('Quality Checks Are not Passed.')
        return super(MrpInh, self).button_mark_done()

    def action_generate_serial(self):
        if self.origin:
            i = 1
            src = self.origin
            mrp = self
            while src != False:
                parent = self.env['mrp.production'].search([('name', '=', src)])
                src = parent.origin
                mrp = parent
            name = mrp.name.split('/')[-1]
        else:
            if self.procurement_group_id.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids:
                name = self.name.split('/')[-1]
            else:
                raise UserError('You are required to enter a source MO number for which, remaining quantity are being manufactured.')
        # if '-' not in self.name.split('/')[-1]:
        #     name = self.name.split('/')[-1] + '-001'
        self.ensure_one()
        lot = self.env['stock.production.lot'].search([('name',  '=', name), ('product_id',  '=', self.product_id.id)])
        if not lot:
            self.lot_producing_id = self.env['stock.production.lot'].create({
                'name': name,
                'product_id': self.product_id.id,
                'company_id': self.company_id.id
            })
        else:
            self.lot_producing_id = lot[0].id
        self.unique_no()
        if self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids:
            self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids.lot_id = self.lot_producing_id
        if self.product_id.tracking == 'serial':
            self._set_qty_producing()

    def unique_no(self):
        for res in self:
            if res.product_id.tracking in ['lot', 'serial']:
                if res.lot_producing_id:
                    if self.origin:
                        parent_list = []
                        parents = self.env['mrp.production'].search(
                            [('origin', '=', res.origin), ('product_id', '=', res.product_id.id), ('state', '!=', 'cancel')])
                        for mrp in parents:
                            if mrp.id != res.id:
                                parent_list.append(mrp.id)
                        if parent_list:
                            last_lot = self.env['mrp.production'].browse(parent_list).mapped('lot_lines').mapped('name')[
                                -1].split('-')
                            pre_num = int(last_lot[0]) + 1
                            pre_seq = int(last_lot[1])
                            for rec in range(0, int(res.product_qty)):
                                if pre_num == 26:
                                    pre_num = 1
                                    pre_seq = pre_seq + 1
                                if pre_num > 9:
                                    a = str(pre_num)
                                else:
                                    a = '0' + str(pre_num)
                                if pre_seq < 10:
                                    a = a + '-' + '000' + str(pre_seq)
                                elif pre_seq < 100 and pre_seq >= 10:
                                    a = a + '-' + '00' + str(pre_seq)
                                elif pre_seq < 1000 and pre_seq >= 100:
                                    a = a + '-' + '0' + str(pre_seq)
                                else:
                                    a = a + '-' + str(pre_seq)
                                print(a)
                                record = self.env['unique.lot'].create({
                                    'name': a,
                                    'lot_id': res.lot_producing_id.id,
                                    'mrp_id': res.id,
                                    'product_id': res.product_id.id,
                                })
                                pre_num = pre_num + 1
                    else:
                        i = 1
                        j = 1
                        src = res.origin
                        mrp = res
                        while src != False:
                            parent = self.env['mrp.production'].search([('name', '=', src)])
                            src = parent.origin
                            mrp = parent
                        for rec in range(0, int(res.product_qty)):
                            if i == 26:
                                i = 1
                                j = j + 1
                            if i > 9:
                                a = str(i)
                            else:
                                a = '0' + str(i)
                            if j < 10:
                                a = a + '-' + '000' + str(j)
                            elif j < 100 and j >= 10:
                                a = a + '-' + '00' + str(j)
                            elif j < 1000 and j >= 100:
                                a = a + '-' + '0' + str(j)
                            else:
                                a = a + '-' + str(j)
                            record = self.env['unique.lot'].create({
                                'name': a,
                                'lot_id': res.lot_producing_id.id,
                                'mrp_id': res.id,
                                'product_id': res.product_id.id,
                            })
                            i = i + 1
                        return super(MrpInh, self).button_mark_done()
                else:
                    raise ValidationError('Please Add Lot/Serial Number.')

    def compute_child_mos(self):
        count = self.env['mrp.production'].search_count([('origin', '=', self.name)])
        self.child_mo_count = count

    # def action_assign(self):
    #     rec = super(MrpInh, self).action_assign()
    #     for line in self.move_raw_ids:
    #         if line.forecast_availability < line.product_uom_qty:
    #             # bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.product_id.product_tmpl_id.id), ('type', '=', 'normal')])
    #             # if bom:
    #             self.show_create_in = True
    #     if not self.is_child_mo_created:
    #         self.create_child_mo()
    #     if self.show_create_in:
    #         self.action_create_internal_transfer()

    def create_child_mo(self):
        product_list = []
        bom = self.env['mrp.bom'].search([])
        for rec in bom:
            product_list.append(rec.product_id.id)

        for line in self.move_raw_ids:
            line_vals = []
            work_vals = []
            if line.product_id.id in product_list:
                bom_id = self.env['mrp.bom'].search([('product_id', '=', line.product_id.id)])
                if bom_id.type == 'normal':
                    for bom_line in bom_id.bom_line_ids:
                        line_vals.append((0, 0, {
                            'product_id': bom_line.product_id.id,
                            'name': bom_line.product_id.name,
                            'location_id': line.location_id.id,
                            'location_dest_id': line.location_dest_id.id,
                            'product_uom_qty': (bom_line.product_qty) * self.product_qty,
                            'product_uom': bom_line.product_uom_id.id,
                        }))
                        line_vals.append(line_vals)
                    for work_line in bom_id.operation_ids:
                        work_vals.append((0, 0, {
                            'name': work_line.name,
                            'quality_point_count': work_line.quality_point_count,
                            'workcenter_id': work_line.workcenter_id.id,
                            'duration_expected': (work_line.time_cycle) * self.product_qty,
                            'product_uom_id': work_line.bom_id.product_uom_id.id,
                            'consumption': 'flexible',
                            # 'product_uom': work_line.product_uom_id.id,
                        }))
                        work_vals.append(work_vals)
                    vals = {
                        # 'picking_for_id': self.id,
                        'product_id': line.product_id.id,
                        'bom_id': bom_id.id,
                        'company_id': self.env.user.company_id.id,
                        'date_planned_start': fields.Date.today(),
                        'move_raw_ids': line_vals,
                        'workorder_ids': work_vals,
                        'location_dest_id': self.location_dest_id.id,
                        'origin': self.name,
                        'product_qty': line.product_uom_qty - line.reserved_availability,
                        'product_uom_id': line.product_id.uom_id.id,
                    }
                    mrp = self.env['mrp.production'].create(vals)
        self.is_child_mo_created = True

    def compute_transfers(self):
        count = self.env['stock.picking'].search_count([('origin', '=', self.name)])
        self.transfer_count = count

    def action_view_child_mo(self):
        return {
            'name': 'Transfers',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'domain': [('origin', '=', self.name)], }

    def action_view_transfers(self):
        return {
            'name': 'Transfers',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.name)], }

    def action_create_internal_transfer(self):
        product_list = []
        bom = self.env['mrp.bom'].search([])
        for rec in bom:
            product_list.append(rec.product_tmpl_id.id)
        picking_delivery = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
        # is_product = False
        # for line in self.move_raw_ids:
        #     if line.product_id.product_tmpl_id.id not in product_list and line.forecast_availability < line.product_uom_qty:
        #         is_product = True
        # if is_product:
        vals = {
            'location_id': picking_delivery.default_location_src_id.id,
            'location_dest_id': picking_delivery.default_location_dest_id.id,
            'partner_id': self.user_id.partner_id.id,
            # 'product_sub_id': self.product_subcontract_id.id,
            'picking_type_id': picking_delivery.id,
            'origin': self.name,
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.move_raw_ids:
            if line.product_id.product_tmpl_id.id not in product_list and line.product_id.type != 'service':
                lines = {
                    'picking_id': picking.id,
                    'product_id': line.product_id.id,
                    'name': self.name,
                    'product_uom': line.product_uom.id,
                    'location_id': picking_delivery.default_location_src_id.id,
                    'location_dest_id': picking_delivery.default_location_dest_id.id,
                    'product_uom_qty': line.product_uom_qty - line.forecast_availability,
                }
                stock_move = self.env['stock.move'].create(lines)
        self.show_create_in = True