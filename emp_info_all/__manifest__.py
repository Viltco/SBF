# -*- coding: utf-8 -*-
{
    'name': "emp_info_all",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr',
                'hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/operation_request.xml',
        'views/iqama.xml',
        'views/visa_request.xml',
        'views/sponsorship_transfer.xml',
        'views/recruiter_visa_request.xml',
        'views/employee_gosi.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
