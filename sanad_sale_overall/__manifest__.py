# -*- coding: utf-8 -*-
{
    'name': "Sanad Sales Overall",

    'summary': """
        Sales Customizations""",

    'description': """
        Sales Customizations
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '14.0.00',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'purchase'],

    # always loaded
    'data': [
        'views/views.xml',
    ],

}
