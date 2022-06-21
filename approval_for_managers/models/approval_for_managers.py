
from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('approve', 'Waiting For Finance Approval'),
        ('manager', 'Waiting For Manager Approval'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('reject', 'Reject'),
        ('cancelled', 'Cancelled'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    approved_by = fields.Many2one('res.users')

    def button_manager(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'approve', 'manager']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.company.currency_id._convert(
                        order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                        order.date_order or fields.Date.today())) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            order.approved_by = order.env.user.id
        return True

    def button_confirm(self):
        self.write({
            'state': 'approve'
        })

    def button_approved(self):
        self.write({
            'state': 'manager'
        })

    def button_reject(self):
        self.write({
            'state': 'draft'
        })

    def manager_reject(self):
        self.write({
            'state': 'reject'
        })

    def button_cancel(self):
        self.write({
            'state': 'cancelled'
        })


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('approve', 'Waiting For Approval'),
        ('sale', 'Sales Order'),
        ('reject', 'Reject'),
        ('done', 'Locked'),
        ('cancelled', 'Cancelled'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_confirm(self):
        self.write({
            'state': 'approve'
        })

    def action_cancel(self):
        self.write({
            'state': 'cancelled'
        })

    def action_drafts(self):
        self.write({
            'state': 'draft'
        })

    def button_approve(self):
        rec = super(SaleOrderInh, self).action_confirm()

    def button_reject(self):
        self.write({
            'state': 'reject'
        })


class MRPProductionInh(models.Model):
    _inherit = 'mrp.production'

    is_check_availability = fields.Boolean(string='Check Availability', default=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approval'),
        ('confirmed', 'Confirmed'),
        ('planned', 'Planned'),
        ('progress', 'In Progress'),
        ('to_close', 'To Close'),
        ('reject', 'Reject'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='State',
        compute='_compute_state', copy=False, index=True, readonly=True,
        store=True, tracking=True,
        help=" * Draft: The MO is not confirmed yet.\n"
             " * Confirmed: The MO is confirmed, the stock rules and the reordering of the components are trigerred.\n"
             " * Planned: The WO are planned.\n"
             " * In Progress: The production has started (on the MO or on the WO).\n"
             " * To Close: The production is done, the MO has to be closed.\n"
             " * Done: The MO is closed, the stock moves are posted. \n"
             " * Cancelled: The MO has been cancelled, can't be confirmed anymore.")

    # my_activity_date_deadline = fields.Date()

    # def action_button_plan(self):
    #     self.write({
    #         'state': 'approve'
    #     })

    def _create_notification(self):
        for res in self:
            act_type_xmlid = 'mail.mail_activity_data_todo'
            summary = 'MO Approval'
            note = 'Manufacturing order no:' + res.name + ' is waiting for Approval.'
            if act_type_xmlid:
                activity_type = self.sudo().env.ref(act_type_xmlid)
            model_id = self.env['ir.model']._get(self._name).id
            users = self.env['res.users'].search([])
            for rec in users:
                if rec.has_group('mrp.group_mrp_manager'):
                    # print(rec.name)
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

    def action_confirm(self):
        for rec in self:
            if rec.mrp_production_source_count > 0:
                rec.button_approve()
            else:
                rec._create_notification()
                rec.write({
                    'state': 'approve'
                })

    def action_assign(self):
        res = super(MRPProductionInh, self).action_assign()
        if self.move_raw_ids:
            for rec in self.move_raw_ids:
                if rec.product_uom_qty == rec.reserved_availability:
                    if self.is_check_availability == False:
                        self.is_check_availability = True
        # for line in self.move_raw_ids:
        #     for move_rec in line.move_line_ids:
        #         if line.should_consume_qty > move_rec.product_uom_qty:
        #             move_rec.qty_done = move_rec.product_uom_qty
        #         else:
        #             move_rec.qty_done = line.should_consume_qty
        return res

    def action_set_to_draft(self):
        self.write({
            'state': 'draft'
        })

    def button_approve(self):
        for rec in self.activity_ids:
            rec.action_done()
        res = super(MRPProductionInh, self).action_confirm()
        # mrp_production_ids = self.procurement_group_id.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids.ids
        # print(mrp_production_ids)
        for res in self.procurement_group_id.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids:
            res.button_approve()
        return res

    def button_reject(self):
        self.write({
            'state': 'reject'
        })

    # @api.model
    # def create(self, vals_list):
    #     res = super(MRPProductionInh, self).create(vals_list)
    #     print('ddddddd', res.mrp_production_source_count)
    #     if res.mrp_production_source_count > 0:
    #         res.button_reject()
    #     return res

class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approve', 'Waiting For Approval'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
        ('reject', 'Reject')
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    available_partner_bank_ids = fields.Many2many('res.bank')

    def action_post(self):
        self.write({
            'state': 'approve'
        })

    def button_approve(self):
        rec = super(AccountMoveInh, self).action_post()

    def button_reject(self):
        self.write({
            'state': 'reject'
        })


class AccountPaymentInh(models.Model):
    _inherit = 'account.payment'

    state = fields.Selection([('draft', 'Draft'),
                              ('approve', 'Waiting For Approval'),
                              ('posted', 'Validated'),
                              ('sent', 'Sent'),
                              ('reconciled', 'Reconciled'),
                              ('cancelled', 'Cancelled'),
                              ('reject', 'Reject')
                              ], readonly=True, default='draft', copy=False, string="Status")

    def action_post(self):
        self.write({
            'state': 'approve'
        })

    def button_approve(self):
        res = super(AccountPaymentInh, self).action_post()
        self.write({
            'state': 'posted'
        })
        return res


        # payments_need_trans = self.filtered(lambda pay: pay.payment_token_id and not pay.payment_transaction_id)
        # transactions = payments_need_trans._create_payment_transaction()
        # res = super(AccountPaymentInh, self - payments_need_trans).action_post()
        # transactions.s2s_do_transaction()
        # # Post payments for issued transactions.
        # transactions._post_process_after_done()
        # payments_trans_done = payments_need_trans.filtered(lambda pay: pay.payment_transaction_id.state == 'approve')
        # super(AccountPaymentInh, payments_trans_done).action_post()
        # payments_trans_not_done = payments_need_trans.filtered(lambda pay: pay.payment_transaction_id.state != 'approve')
        # payments_trans_not_done.action_cancel()
        # return res

        # AccountMove = self.env['account.move'].with_context(default_type='entry')
        # for rec in self:
        #
        #     if rec.state != 'approve':
        #         raise UserError(_("Only a draft payment can be posted."))
        #
        #     if any(inv.state != 'posted' for inv in rec.invoice_ids):
        #         raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))
        #
        #     # keep the name in case of a payment reset to draft
        #     if not rec.name:
        #         # Use the right sequence to set the name
        #         if rec.payment_type == 'transfer':
        #             sequence_code = 'account.payment.transfer'
        #         else:
        #             if rec.partner_type == 'customer':
        #                 if rec.payment_type == 'inbound':
        #                     sequence_code = 'account.payment.customer.invoice'
        #                 if rec.payment_type == 'outbound':
        #                     sequence_code = 'account.payment.customer.refund'
        #             if rec.partner_type == 'supplier':
        #                 if rec.payment_type == 'inbound':
        #                     sequence_code = 'account.payment.supplier.refund'
        #                 if rec.payment_type == 'outbound':
        #                     sequence_code = 'account.payment.supplier.invoice'
        #         rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
        #         if not rec.name and rec.payment_type != 'transfer':
        #             raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))
        #
        #     moves = AccountMove.create(rec._prepare_payment_moves())
        #     moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()
        #
        #     # Update the state / move before performing any reconciliation.
        #     move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
        #     rec.write({'state': 'posted', 'move_name': move_name})
        #
        #     if rec.payment_type in ('inbound', 'outbound'):
        #         # ==== 'inbound' / 'outbound' ====
        #         if rec.invoice_ids:
        #             (moves[0] + rec.invoice_ids).line_ids \
        #                 .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id and not (line.account_id == line.payment_id.writeoff_account_id and line.name == line.payment_id.writeoff_label))\
        #                 .reconcile()
        #     elif rec.payment_type == 'transfer':
        #         # ==== 'transfer' ====
        #         moves.mapped('line_ids')\
        #             .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id)\
        #             .reconcile()
        #
        # return True


    def button_reject(self):
        self.write({
            'state': 'reject'
        })

class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('approve', 'Waiting For Approval'),
        ('done', 'Done'),
        ('reject', 'Reject'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state', copy=False,
        index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    def button_validate(self):
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # Sanity checks.
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking

            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(
                float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(
                float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line
                in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking

            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(
                        lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(
                    products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(
                    pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _(
                    '\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(
                    pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (
                ', '.join(pickings_without_lots.mapped('name')),
                ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())
        self.state = 'approve'

    def button_approved(self):
        rec = super(StockPickingInh, self).button_validate()
        backorder = self.env['stock.picking'].search([('backorder_id', '=', self.id)])
        if backorder:
            backorder.do_unreserve()
        return rec

    def button_reject(self):
        self.write({
            'state': 'reject'
        })


class StockBackorderConfirmationInh(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self):
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.backorder_confirmation_line_ids:
            if line.to_backorder is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        for pick_id in pickings_not_to_do:
            moves_to_log = {}
            for move in pick_id.move_lines:
                if float_compare(move.product_uom_qty,
                                 move.quantity_done,
                                 precision_rounding=move.product_uom.rounding) > 0:
                    moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
            pick_id._log_less_quantities_than_expected(moves_to_log)

        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate).with_context(
                skip_backorder=True)
            if pickings_not_to_do:
                pickings_to_validate = pickings_to_validate.with_context(
                    picking_ids_not_to_backorder=pickings_not_to_do.ids)

            return pickings_to_validate.button_approved()
        return True

    def process_cancel_backorder(self):
        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            return self.env['stock.picking'] \
                .browse(pickings_to_validate) \
                .with_context(skip_backorder=True, picking_ids_not_to_backorder=self.pick_ids.ids) \
                .button_approved()
        return True


class StockImmediateTransferInh(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        pickings_to_do = self.env['stock.picking']
        pickings_not_to_do = self.env['stock.picking']
        for line in self.immediate_transfer_line_ids:
            if line.to_immediate is True:
                pickings_to_do |= line.picking_id
            else:
                pickings_not_to_do |= line.picking_id

        for picking in pickings_to_do:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty

        pickings_to_validate = self.env.context.get('button_validate_picking_ids')
        if pickings_to_validate:
            pickings_to_validate = self.env['stock.picking'].browse(pickings_to_validate)
            pickings_to_validate = pickings_to_validate - pickings_not_to_do
            return pickings_to_validate.with_context(skip_immediate=True).button_approved()
        return True

