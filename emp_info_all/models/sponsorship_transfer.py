from odoo import api, fields, models


class SponsorshipTransfer(models.Model):
    _name = "sponsorship.transfer"
    _description = "Sponsorship Transfer"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    recruiter = fields.Many2one('hr.department', string='Recruiter')
    handle_by = fields.Selection([
        ('individual', 'Individual'),
        ('multiple', 'Multiple'),
    ])

    description = fields.Text(string='Description')

    state = fields.Selection(
        [('draft', 'Draft'), ('waiting_approval', 'Waiting Approval'), ('approved', 'Approved'),('reject', 'Rejected')],
        default='draft')

    def action_submit(self):
        self.state = 'waiting_approval'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'reject'
