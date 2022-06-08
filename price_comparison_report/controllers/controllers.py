# -*- coding: utf-8 -*-
# from odoo import http


# class PriceComparisionReport(http.Controller):
#     @http.route('/price_comparison_report/price_comparison_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/price_comparison_report/price_comparison_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('price_comparison_report.listing', {
#             'root': '/price_comparison_report/price_comparison_report',
#             'objects': http.request.env['price_comparison_report.price_comparison_report'].search([]),
#         })

#     @http.route('/price_comparison_report/price_comparison_report/objects/<model("price_comparison_report.price_comparison_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('price_comparison_report.object', {
#             'object': obj
#         })
