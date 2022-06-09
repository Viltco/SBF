from odoo import api, fields, models


class RecruiterVisaRequest(models.Model):
    _name = "recruiter.request"
    _description = "Recruiter Request"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)

    emp_code = fields.Char(string='Employee Code', related='employee_id.pin')
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Many2one('hr.department', related='employee_id.department_id')
    job_position = fields.Many2one('hr.job', related='employee_id.job_id')

    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', related='employee_id.country_id')
    email = fields.Char(string='Email' ,related='employee_id.work_email')
    passport_no = fields.Char(string='Passport Number' ,related='employee_id.passport_id')
    fiscal_year = fields.Date(string='Fiscal Year')
    request_by = fields.Many2one('hr.department', string='Request By')

    visa_for = fields.Selection([
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
    ])
    type = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ])
    type_of_visa = fields.Selection([
        ('businessvisitvisa', 'Business Visit Visa'),
        ('workvisitvisa', 'Work Visit Visa'),
        ('newworkvisa', 'New Work Visa'),
    ])

    dep_date = fields.Date(string='Departure Date')
    visa_title = fields.Char(string='Visa Title')
    country = fields.Many2one(
        'res.country', 'Country')
    return_date = fields.Date(string='Return Date')
    visa_no = fields.Integer(string='Visa Number')
    visa_duration = fields.Integer(string='Visa Duration')
    approve_date_from = fields.Date(string='Approve Date From', readonly="1")
    approve_date_to = fields.Date(string='Approve Date To', readonly="1")

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('tosubmit', 'ToSubmit'), ('confirm', 'Confirm'),('reject', 'Rejected') ],
        default='tosubmit')

    def action_submit(self):
        self.state = 'confirm'

    def action_reject(self):
        self.state = 'reject'


