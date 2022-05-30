from odoo import models, fields, api
from datetime import datetime


class notify_alert_quality(models.Model):
    _inherit = "quality.alert"

    my_activity_date_deadline = fields.Date()
    def _create_notification(self):
        act_type_xmlid = 'mail.mail_activity_data_todo'
        summary = 'Reserved DO Notification'
        note = '25 Days passed.In 5 days left, DO no: ' + self.name + ' will be unreserved Automatically.'
        if act_type_xmlid:
            activity_type = self.sudo().env.ref(act_type_xmlid)
        model_id = self.env['ir.model']._get(self._name).id
        users = self.env['res.users'].search([])
        for rec in users:
            if rec.has_group('quality.group_quality_manager'):
                create_vals = {
                    'activity_type_id': activity_type.id,
                    'summary': summary or activity_type.summary,
                    'automated': True,
                    'note': note,
                    'date_deadline': datetime.today(),
                    'res_model_id': model_id,
                    'res_id': self.id,
                    'user_id': rec.id,
                }
                activities = self.env['mail.activity'].create(create_vals)

    @api.model
    def create(self, vals):
        res = super(notify_alert_quality, self).create(vals)
        res._create_notification()
        return res