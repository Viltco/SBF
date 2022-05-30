# -*- coding: utf-8 -*-

{
    "name": "e-Invoice KSA",
    "version": "14.0.0.0",
    "depends": [
        'base', 'web', 'account', 'invoice_barcode_qr'
    ],
    "author": "Viltco",
    "category": "Accounting",
    "website": "https://www-viltco.com/",
    "support": "www.viltco.com",
    "images": ["static/description/assets/main_screenshot.gif","static/description/assets/main_screenshot.png", "static/description/assets/ghits_desktop_inv.jpg",
               "static/description/assets/ghits_labtop1.jpg"],
    "summary": "e-Invoice in Kingdom of Saudi Arabia KSA | tax invoice | vat  | electronic | e invoice | accounting | tax | free | ksa | sa |Zakat, Tax and Customs Authority | الفاتورة الضريبية | الفوترة  الالكترونية |   هيئة الزكاة والضريبة والجمارك",
    "description": """
    e-Invoice in Kingdom of Saudi Arabia
    and prepare tax invoice to be ready for the second phase.
    Zakat, Tax and Customs Authority
    الفوترة الإلكترونية - الفاتورة الضريبية - المملكة العربية السعودية
    المرحلة الاولي -  مرحلة الاصدار 
    هيئة الزكاة والضريبة والجمارك

    Versions History --------------------
    
     * version 14.0.0.0: 06-DEC-2021
         - Initial version compatible with odoo v14 , tax invoice report, QR code    
    """
    ,
    "data": [
        "view/partner.xml",
        "report/base_document_layout.xml",
        "report/account_move.xml",

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    'assets': {
        'web.report_assets_common': [
            'einv_sa/static/css/report_style.css',
        ],
    },
}
