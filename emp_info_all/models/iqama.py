from odoo import api, fields, models


class IqamaRequest(models.Model):
    _name = "iqama.request"
    _description = "Iqama Request"
    _rec_name = 'iqama_type'

    iqama_type = fields.Selection([
        ('employee', 'Employee'),
        ('family', 'Family'),
        ('newbornbaby', 'New Born Baby'),
    ], required=True, )

    employee_id = fields.Many2one('hr.employee', string='Employee')
    emp_code = fields.Char(string='Employee Code', related='employee_id.pin')
    emp_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    emp_department = fields.Many2one('hr.department', related='employee_id.department_id')
    job_position = fields.Many2one('hr.job', related='employee_id.job_id')

    office = fields.Char(string='Office', readonly="1")
    name_as_passport = fields.Char(string='Name(As in Passport)')
    arabic_name = fields.Char(string='Arabic Name')
    nationality = fields.Many2one(
        'res.country', 'Nationality', related='employee_id.country_id')
    religion = fields.Selection([
        ('muslim', 'Muslim'),
        ('non-muslim', 'Non-Muslim'),
        ('other', 'Other'),
    ])
    date_of_birth = fields.Date(string='Date of Birth', related='employee_id.birthday')
    profession = fields.Char(string='Profession', related='employee_id.job_title')

    iqama_number = fields.Integer(string='Iqama Number')
    serial_number = fields.Integer(string='Serial Number')
    iqama_position = fields.Char(string='Iqama Position')
    place_of_issue = fields.Char(string='Place of Issue')
    date_of_issue = fields.Date(string='Date of Issue')
    date_of_expiry = fields.Date(string='Date of Expiry')
    date_of_expiry_hijri = fields.Date(string='Date of Expiry(Hijri)')

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_approval', 'Waiting Approval'), ('approved', 'Approved'),
         ('reject', 'Rejected')],
        default='draft')

    def action_confirm(self):
        self.state = 'waiting_approval'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'reject'
