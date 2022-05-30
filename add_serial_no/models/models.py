# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import re


# class StockProductionLotInh(models.Model):
#     _inherit = 'stock.production.lot'
#
#     @api.constrains('name')
#     def check_code(self):
#         if self.name:
#             code = self.env['stock.production.lot'].search([('name', '=', self.name)])
#             if len(code) > 1:
#                 raise UserError('Lot Already Exists')


class StockMoveInh(models.Model):
    _inherit = 'stock.move'

    first = fields.Char('Prefix', default='SRN')
    qty = fields.Integer('Quantity')

    @api.onchange('first')
    def set_upper(self):
        self.first = str(self.first).upper()
        return

    def action_add_lines(self):
        val_list = []
        counter = 0
        lot = self.env['custom.production.lot'].search([], order='id desc')
        last_lot = ''
        if lot:
            last_lot = lot[0].code
        else:
            last_lot = 0
        # for rec in lot:
        #     # res = re.findall('(\d+|[A-Za-z]+)', rec.name)
        #     if res[0] == 'SRN':
        #         last_lot = res[0] + str(int(res[1]))
        #         break
        for i in range(0, int(self.qty)):
            counter = counter + 1
            name = self.first + str(int(last_lot)+int(counter))
            print(name)
            self.env['custom.production.lot'].create({
                'name': name,
                'code': str(int(last_lot) + counter),
            })
            val_list.append((0, 0, {
                'lot_name': name,
                'product_uom_id': self.product_uom.id,
                'product_id': self.product_id.id,
                'qty_done': 1
            }))
        self.move_line_nosuggest_ids = val_list
        # for l in vals:

    def action_clear_lines_show_details(self):
        pass


class StockProductionLotCustomInh(models.Model):
    _name = 'custom.production.lot'

    name = fields.Char()
    code = fields.Char()

