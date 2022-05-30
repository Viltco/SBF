from odoo import models, fields, api
from odoo.osv import expression



class SbHrEmployeeInherited(models.Model):
    _inherit="hr.employee"
    
    '''
       search employee with 'Name' or with 'Pin Code'
    '''
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('pin', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
    
    
# 
#     def init(self):
#          
#         self.env.cr.execute("ALTER TABLE hr_employee DROP CONSTRAINT hr_employee_user_uniq")
#        


class SbMrpWorkCentre(models.Model):
    _inherit = 'mrp.workcenter'
    
    employee_ids = fields.Many2many('hr.employee','emp_workcenter_rel', 'mrp_workcenter_id', 'emp_id', string='Employees')
    
    
