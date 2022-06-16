from odoo import models, api


class PriceComparisonReport(models.AbstractModel):
    _name = 'report.price_comparison_report.price_comparison_id_landscape'
    _description = 'Price Comparison Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('printed---------------------------------------------')
        records = self.env['purchase.requisition'].search([('id', 'in', docids)])
        print(records)
        origin_list = []
        for rec in records:
            origin_list.append((rec.name))
        print(origin_list)
        rfq = self.env['purchase.order'].search([('origin', 'in', origin_list)])

        return {
            'doc_ids': docids,
            'doc_model': 'purchase.requisition',
            'docs': records,
            'orders': rfq,
        }
