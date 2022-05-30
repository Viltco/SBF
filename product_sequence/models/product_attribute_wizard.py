
from odoo import models, fields, api


class ProductAttributeWizard(models.TransientModel):
    _name = 'product.attribute.wizard'

    value_ids = fields.Many2many('product.attribute.value')
    attribute_id = fields.Many2one('product.attribute')

    def action_create_attribute(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        if rec_model.attribute_line_ids:
            for rec in rec_model.attribute_line_ids:
                if rec.attribute_id.id == self.attribute_id.id:
                    att_list = []
                    for attr in rec.value_ids:
                        att_list.append(attr.id)
                    for x in self.value_ids:
                        att_list.append(x.id)
                    rec.write({
                        'value_ids': att_list,
                    })
        else:
            vals = {
                'attribute_id': self.attribute_id.id,
                'value_ids': self.value_ids.ids,
                'product_tmpl_id': rec_model.id
            }
            # rec_model.attribute_line_ids = val_list
            # for res in rec_model.attribute_line_ids:
            #     if res.attribute_id.id == self.attribute_id.id:
            #         # att_list = []
            #         # for attr in rec.value_ids:
            #         #     att_list.append(attr.id)
            #         # for x in self.value_ids:
            #         #     att_list.append(x.id)
            #         res.update({
            #             'value_ids': self.value_ids.ids,
            #         })
            pro = self.env['product.template.attribute.line'].create(vals)
        self.assign_sequence_in_variant()

    def assign_sequence_in_variant(self):
        model = self.env.context.get('active_model')
        rec_model = self.env[model].browse(self.env.context.get('active_id'))
        count = 0
        print(rec_model.product_variant_ids)
        for variant in rec_model.product_variant_ids:
            count += 1
            variant.product_seq = str(00) + str(00) + str(0) + str(count)
            variant.item_code = rec_model.product_temp_seq + variant.product_seq
        return

