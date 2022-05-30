# -*- coding: utf-8 -*-
{
    'name': 'Invoice & Bill: Barcode / QR code',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'summary': """ This modules enables print invoice/bill code128 barcode as its name and add QR for invoice/bill URL""",
    'description': """    invoice/bill reports with code128 barcode reflect invoice/bill code and QR code for its URL    """,
    'author': 'Eng. Ahmed Sherby, EIS',
    'website': "https://Egypt4is.com",
    'company': 'EIS',
    'maintainer': 'EIS',
    'depends': ['base', 'account'],
    'data': [
        'views/res_config_settings_views.xml',
        'reports/inherited_invoice_report_barcode_qr.xml',
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
