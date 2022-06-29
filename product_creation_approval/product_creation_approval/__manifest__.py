# -*- coding: utf-8 -*-
{
    'name': "Product Creation Approval",

    'summary': """
        Need Approval On Product Creation""",

    'description': """
        Need Approval On Product Creation
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'mrp','account'],

    # always loaded
    'data': [
        'views/product_creation_approval_views.xml',
    ],
}
