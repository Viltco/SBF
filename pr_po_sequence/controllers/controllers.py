# -*- coding: utf-8 -*-
# from odoo import http


# class PrPoSequence(http.Controller):
#     @http.route('/pr_po_sequence/pr_po_sequence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pr_po_sequence/pr_po_sequence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pr_po_sequence.listing', {
#             'root': '/pr_po_sequence/pr_po_sequence',
#             'objects': http.request.env['pr_po_sequence.pr_po_sequence'].search([]),
#         })

#     @http.route('/pr_po_sequence/pr_po_sequence/objects/<model("pr_po_sequence.pr_po_sequence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pr_po_sequence.object', {
#             'object': obj
#         })
