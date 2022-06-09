from odoo import api, fields, models


class OperationRequest(models.Model):
    _name = "operation.request"
    _description = "Operation Request"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_code = fields.Char(string='Employee Code', related='employee_id.pin')
    employee_ems_code = fields.Integer(string='Employee Ems Code', readonly="1")
    department = fields.Many2one('hr.department', related='employee_id.department_id')
    job_position = fields.Many2one('hr.job', related='employee_id.job_id')



    operation = fields.Selection([
        ('changingprofession', 'Changing Profession'),
        ('familyvisarequest', 'Family Visa Request'),
        ('lossingiqama', 'Lossing Iqama'),
        ('saudizationcertification', 'Saudization Certification'),
    ])
    expense_needed = fields.Boolean(string='Expense Needed')
    handle_by = fields.Selection([
        ('other', 'Other')
    ])

    description = fields.Text(string='Description')

    reason_for_saudi_certification = fields.Selection([
        ('getatenderdocument', 'Get a Tender Document'),
        ('other', 'Other'),
    ])
    client_name = fields.Char(string='Client Name')
    project_name = fields.Char(string='Project Name')

    state = fields.Selection(
        [('new', 'New'), ('waiting_approval', 'Waiting For Approval'), ('approved', 'Approved'),('reject', 'Rejected')],
        default='new')

    def action_submit(self):
        self.state = 'waiting_approval'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'reject'
