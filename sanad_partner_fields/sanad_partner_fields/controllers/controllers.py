# -*- coding: utf-8 -*-
# from odoo import http


# class SanadPartnerFields(http.Controller):
#     @http.route('/sanad_partner_fields/sanad_partner_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sanad_partner_fields/sanad_partner_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sanad_partner_fields.listing', {
#             'root': '/sanad_partner_fields/sanad_partner_fields',
#             'objects': http.request.env['sanad_partner_fields.sanad_partner_fields'].search([]),
#         })

#     @http.route('/sanad_partner_fields/sanad_partner_fields/objects/<model("sanad_partner_fields.sanad_partner_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sanad_partner_fields.object', {
#             'object': obj
#         })
