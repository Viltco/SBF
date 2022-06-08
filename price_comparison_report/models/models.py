# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class price_comparison_report(models.Model):
#     _name = 'price_comparison_report.price_comparison_report'
#     _description = 'price_comparison_report.price_comparison_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
