# -*- coding: utf-8 -*-
{
    'name': "PR PO Sequence",

    'summary': """
        This Module Generates PO and PR Sequence""",

    'description': """
        This Module Generates PO and PR Sequence
    """,

    'author': "Viltco",
    'website': "http://www.viltco.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '14.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'material_purchase_requisitions'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
