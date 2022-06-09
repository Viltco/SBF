from odoo import api, fields, models


class GosiLines(models.Model):
    _name = "gosi.lines"
    _description = "Gosi Lines"


    payslip_id = fields.Many2one('hr.payslip', string='PaySlip')
    date = fields.Date(string='Date')
    gosi_amount = fields.Integer(string='Gosi Amount')

    employee_gosi_id = fields.Many2one('employee.gosi')

