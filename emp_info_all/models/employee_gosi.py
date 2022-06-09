from odoo import api, fields, models


class EmployeeGosi(models.Model):
    _name = "employee.gosi"
    _description = "Employee Gosi"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    emp_arabic_name = fields.Char(string='Employee Arabic Name', readonly="1")
    emp_code = fields.Char(string='Employee Code', related='employee_id.pin')
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Many2one('hr.department', related='employee_id.department_id')
    job_position = fields.Many2one('hr.job', related='employee_id.job_id')

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', related='employee_id.country_id')
    passport_no = fields.Char(string='Passport Number' ,related='employee_id.passport_id')

    type = fields.Selection([
        ('saudi', 'Saudi'),
        ('other', 'Other'),
    ])
    family_card_id = fields.Integer(string='Family Card ID')

    issue_date = fields.Date(string='Issue Date')
    date_birth = fields.Date(string='Date of Birth')
    date_birth_hijri = fields.Date(string='Date of Birth(Hijri)')
    gosi_no = fields.Integer(string='Gosi Number')

    gosi_lines_id = fields.One2many('gosi.lines', 'employee_gosi_id', string='Gosi')
