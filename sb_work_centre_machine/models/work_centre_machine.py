# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError,UserError


class SbWorkCentreMachine(models.Model):
    _name = 'centre.machine'
    _description = 'Work Centre Machine'

    name = fields.Char(string="Machine", required = True)
    workcenter_id= fields.Many2one('mrp.workcenter', stirng="work_center")

class SbMrpWorkorder(models.Model):
    _inherit= 'mrp.workorder'
    
    workcenter_machine_id = fields.Many2one('centre.machine' , string="Workcenter Machine")
    employee_id =  fields.Many2one('hr.employee',string='Employees')
    employee_code = fields.Char(string='Employee code', related = 'employee_id.pin')
    workcenter_emp_ids = fields.Many2many('hr.employee',string ='workcenter emp ids', related = 'workcenter_id.employee_ids')
    
    def button_start(self):
        if self.employee_id and self.workcenter_machine_id:
            res = super().button_start()
            return res
        else:
            if (not self.employee_id)  and  (not self.workcenter_machine_id):
                raise ValidationError(_('Please select Work Machine and Employee'))
            elif not self.employee_id:
                raise ValidationError(_('Please select Employee'))
            elif not self.workcenter_machine_id:
                raise ValidationError(_('Please select Work Center Machine'))  
        
            raise ValidationError(_('you cannot start this process'))
    
#     @api.onchange('workcenter_id')
#     def onchange_workcentre_id(self):
#         self.employee_id = False
#         if self.workcenter_id:
#             return {'domain': {'employee_id' :[('id' ,'in', self.workcenter_id.employee_ids.ids)]}}
     
#     
    
    
