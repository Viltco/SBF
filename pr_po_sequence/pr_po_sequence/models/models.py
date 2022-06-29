# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class HRDPTInherit(models.Model):
    _inherit = 'hr.department'

    dept_code = fields.Char(string='Department Code')

    @api.constrains('dept_code')
    def check_dept_code(self):
        if self.dept_code:
            code = self.env['hr.department'].search([('dept_code', '=', self.dept_code)])
            if len(code) > 1:
                raise UserError('Department Code Already Exists.')


class MPRInherit(models.Model):
    _inherit = 'material.purchase.requisition'

    @api.model
    def create(self, vals):
        res = super(MPRInherit, self).create(vals)
        pos = str(self.env['ir.sequence'].next_by_code('requisition.sequence'))
        pre = str(res.name[:4])
        dept = str(self.env.user.department_id.dept_code)
        new_name = (pre + '1' + dept + pos)
        print(new_name)
        res.update({
            'name': new_name
        })
        return res


class POInherit(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        res = super(POInherit, self).create(vals)
        pos = str(self.env['ir.sequence'].next_by_code('purchase.sequence'))
        pre = str(res.name[:4])
        record = self.env['res.users'].browse(vals['user_id'])
        dept = False
        if record.employee_id:
            dept = record.department_id.dept_code
        new_name = (pre + '2' + str(dept) + pos[-3:])
        res.update({
            'name': new_name
        })
        return res
