# -*- coding: utf-8 -*-


import datetime
from lxml import etree
from odoo import models, fields, api, _ ,tools
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
from odoo.tools import float_compare
# import simplejson
import json


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    # State Field

    is_tmpl = fields.Boolean(string='Is Template', compute='_compute_is_tmpl')

    state = fields.Selection([('draft', 'Draft'),
                              ('to_approve', 'Waiting For Approval'),
                              ('done', 'Done'),
                              ('rejected', 'Rejected'),
                              ], string='State', default='draft', tracking=True, readonly=True, index=True, copy=False)


    def _compute_is_tmpl(self):
        if self.product_tmpl_id:
            self.is_tmpl = True
        else:
            self.is_tmpl = False

    def button_confirm(self):
        self.write({
            'state': 'to_approve'
        })

    def button_draft(self):
        self.write({
            'state': 'draft'
        })
        self.is_archive = False
        self.active = False

    def button_approve(self):
        self.write({
            'state': 'done'
        })
        self.is_archive = False
        self.active = True

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    @api.model
    def create(self, vals):
        result = super(ProductProductInherit, self).create(vals)
        result.active = False
        result.is_archive = True
        return result


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    # State Field

    # is_confirm = fields.Boolean(string='Is Confirm', default=False)
    is_archive = fields.Boolean()
    @tools.ormcache()
    def _get_default_uom_id(self):
        # Deletion forbidden (at least through unlink)
        return self.env.ref('uom.product_uom_unit')
    
    
    
    state = fields.Selection([('draft', 'Draft'),
                              ('to_approve', 'Waiting For Approval'),
                              ('done', 'Done'),
                              ('rejected', 'Rejected'),
                              ], string='State', default='draft', tracking=True, readonly=True, index=True, copy=False)
     
     
     
    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price',
        help="Price at which the product is sold to customers." , tracking=True)
    
    
    standard_price = fields.Float(
        'Cost', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits='Product Price', groups="base.group_user",
        help="""In Standard Price & AVCO: value of the product (automatically computed in AVCO).
        In FIFO: value of the last unit that left the stock (automatically computed).
        Used to value the product when the purchase cost is not known (e.g. inventory adjustment).
        Used to compute margins on sale orders.""" , tracking=True)
    
    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for all stock operations.", tracking=True)
    
    
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')], string='Product Type', default='consu', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.',tracking=True)
    
    
    default_code = fields.Char(
        'Internal Reference', compute='_compute_default_code',
        inverse='_set_default_code', store=True , tracking=True)
    
    barcode = fields.Char('Barcode', compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode', tracking=True)
    
    
    
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", help="Ensure the traceability of a storable product in your warehouse.", default='none', required=True, tracking=True)
    
    
    sale_ok = fields.Boolean('Can be Sold', default=True, tracking =True)
    purchase_ok = fields.Boolean('Can be Purchased', default=True ,tracking =True)
    
     
    def button_confirm(self):
        self.write({
            'state': 'to_approve'
        })
        # return{
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        #     'params': {'turn_view_readonly': True}
        # }

    def button_draft(self):
        self.write({
            'state': 'draft'
        })
        self.is_archive = False
        self.active = False
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    def button_approve(self):
        self.write({
            'state': 'done'
        })
        self.active = True
        self.is_archive = False
        self.product_variant_id.button_approve()

    def button_reject(self):
        self.write({
            'state': 'rejected'
        })

    @api.model
    def create(self, vals):
        result = super(ProductTemplateInherit, self).create(vals)
        result.active = False
        result.product_variant_id.active = False
        result.is_archive = True
        return result
    
    
#     @api.onchange('attribute_line_ids')
    def track_attribute_line(self,attribute_name,old_val ,new_val):
#         for attribute_line in self:
#             if attribute_line.attribute_line_ids:
#                 s=''
        msg_body = f'{attribute_name} : old value = "{old_val}" ___changed to {new_val}'
        self.message_post(body = msg_body)
        return True
#     
    
    
    
     
    # @api.model
    # def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
    #     context = self._context
    #     res = super(ProductTemplateInherit, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
    #     if view_type == 'form':
    #         doc = etree.XML(res['arch'])
    #         if self.browse(context.get('params').get('id')).state in ['to_approve', 'done']:
    #             for node in doc.xpath("//field"):
    #                 modifiers = json.loads(node.get("modifiers"))
    #                 modifiers['readonly'] = True
    #                 node.set("modifiers", json.dumps(modifiers))
    #         res['arch'] = etree.tostring(doc)
    #     return res
