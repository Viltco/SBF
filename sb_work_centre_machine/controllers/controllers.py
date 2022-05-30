# -*- coding: utf-8 -*-
# from odoo import http


# class SbWorkCentreMachine(http.Controller):
#     @http.route('/sb_work_centre_machine/sb_work_centre_machine/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sb_work_centre_machine/sb_work_centre_machine/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sb_work_centre_machine.listing', {
#             'root': '/sb_work_centre_machine/sb_work_centre_machine',
#             'objects': http.request.env['sb_work_centre_machine.sb_work_centre_machine'].search([]),
#         })

#     @http.route('/sb_work_centre_machine/sb_work_centre_machine/objects/<model("sb_work_centre_machine.sb_work_centre_machine"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sb_work_centre_machine.object', {
#             'object': obj
#         })
