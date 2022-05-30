# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MRPInherit(models.Model):
    _inherit = 'mrp.production'

    def jtc_splits_name(self):
        ref_code = self.name[6:]
        return ref_code

    def total_join(self):
        return int(self.product_qty)

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
