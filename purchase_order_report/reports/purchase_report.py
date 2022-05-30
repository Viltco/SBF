# -*- coding: utf-8 -*-
from odoo import api, models
from num2words import num2words


class PurchaseReportCustom(models.AbstractModel):
    _name = 'report.purchase_order_report.report_purchase_order_inh'

    def get_amount_in_word(self, doc):
        text = num2words(doc.amount_total)
        return text.title()

    @api.model
    def _get_report_values(self, docids, data=None):
        doc = self.env["purchase.order"].search([("id", "in", docids)])
        product_list = []
        for rec in doc.order_line:
            product_list.append(rec.product_id.id)
        product_list = list(dict.fromkeys(product_list))
        all_product_list = []
        for rec in product_list:
            sub_list = []
            qty = 0
            code = ''
            uom = ''
            price = 0
            disc = 0
            total = 0
            date = ''
            desc = ''
            for line in doc.order_line:
                if line.product_id.id == rec:
                    qty = qty + line.product_qty
                    code = line.product_id.item_code
                    uom = line.product_uom.name
                    price = line.price_unit
                    disc = line.discount + disc
                    total = line.price_subtotal
                    date = line.date_planned.date()
                    desc = line.name
            sub_list.append(code)
            sub_list.append(qty)
            sub_list.append(uom)
            sub_list.append(price)
            sub_list.append(disc)
            sub_list.append(total)
            sub_list.append(date)
            sub_list.append(desc)
            all_product_list.append(sub_list)
        amount_in_words = self.get_amount_in_word(doc)
        print(all_product_list)
        total_dis = 0
        for dis_line in doc.order_line:
            total_dis = total_dis + dis_line.discount
        return {
            'doc_ids': self.ids,
            'docs': doc,
            'doc_model': 'purchase_order_report.purchase.order',
            'products': all_product_list,
            'discount': total_dis,
            'amount_in_words': amount_in_words,
            # 'purchase_product': self.get_purchase_products,
        }
