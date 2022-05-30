# -*- coding: utf-8 -*-


import ast
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MRPInherit(models.Model):
    _inherit = 'mrp.production'

    def jtc_splits_name(self):
        ref_code = self.name[6:]
        return ref_code

    # def total_join(self):
    #     return int(self.product_qty)

    def get_rejected(self, oper, workcenter):
        qty = 0
        for rec in self.reason_lines:
            if rec.name == oper and rec.workcenter_id.id == workcenter:
                qty = qty + rec.qty
        return qty


    def jtc_splits(self):
        list = []
        i = 1
        for rec in range(0, int(self.product_qty)):
            if i > 9:
                a = str(i)
            else:
                a = '0' + str(i)
            list.append(a + '-' + self.name.split('/')[-1])
            i = i + 1
        return list

    # def remove_duplicate(self):
    #     opr_list = []
    #     wrk_list = []
    #     for rec in self.produced_lines:
    #         if rec.name not in opr_list:
    #             opr_list.append({
    #                     'operation': rec.name,
    #                 })
    #
    #         if rec.workcenter_id.id not in wrk_list:
    #             wrk_list.append({
    #                     'workcenter_id': rec.workcenter_id.id,
    #                 })
    #
    #     list_org_updated_opr = [str(item) for item in opr_list]
    #     unique_set_opr = set(list_org_updated_opr)
    #     unique_list_opr = [ast.literal_eval(item) for item in unique_set_opr]
    #     print(unique_list_opr)
    #
    #     list_org_updated_wrk = [str(item) for item in wrk_list]
    #     unique_set_wrk = set(list_org_updated_wrk)
    #     unique_list_wrk = [ast.literal_eval(item) for item in unique_set_wrk]
    #     print(unique_list_wrk)
    #
    #     return unique_list

    def remove_dups(self):
        val_list = []
        val = []
        for rec in self.produced_lines:
            if rec.workcenter_id.id not in val_list:
                val_list.append({
                    'workcenter_id': rec.workcenter_id.id,
                    'operation': rec.name,
                })

        for record in self.produced_lines:
            if record.workcenter_id.id not in val:
                val.append({
                    'workcenter_id': record.workcenter_id.id,
                    'work_name': record.workcenter_id.name,
                    'operation': record.name,
                    'employee': record.employee_id.name,
                    'code': record.employee_id.pin,
                    'quantity': record.qty,
                })

        new_list = []
        opr_list = []
        for l in val_list:
            qty = 0
            if l['workcenter_id'] not in new_list or l['operation'] not in opr_list:
                for i in val:
                    if i['workcenter_id'] == l['workcenter_id'] and i['operation'] == l['operation']:
                        new_list.append(l['workcenter_id'])
                        opr_list.append(l['operation'])
                        qty = qty + i['quantity']
                for j in val:
                    if j['workcenter_id'] == l['workcenter_id'] and j['operation'] == l['operation']:
                        j['quantity'] = qty

        list_org_updated = [str(item) for item in val]
        unique_set = set(list_org_updated)
        unique_list = [ast.literal_eval(item) for item in unique_set]
        # sorted_list = sorted(unique_list, key=lambda i: i['seq'])
        return unique_list

