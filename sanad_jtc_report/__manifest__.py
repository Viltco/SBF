# -*- coding: utf-8 -*-
{
    'name': "Job Travel Card",

    'summary': """
        Job Travel Card Report""",

    'description': """
               Job Travel Card Report   
                 """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mrp',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        'views/jtc_view.xml',
        'reports/jtc_bag_template.xml',
        'reports/jtc_dis_spout_template.xml',
        'reports/jtc_filling_spout_template.xml',
        'reports/jtc_reports.xml',
        'reports/jtc_wall_template.xml',
    ],

}
