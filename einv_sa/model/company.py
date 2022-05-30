# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class ResCompany(models.Model):
    _inherit = 'res.company'

    building_no = fields.Char(string="Building no", related='partner_id.building_no', help="Building No")
    district = fields.Char(string="District", related='partner_id.district', help="District")
    code = fields.Char(string="Code", related='partner_id.code', help="Code")

    additional_no = fields.Char(string="Additional No")
    other_id = fields.Char(string="Other Seller ID")

    name_arabic = fields.Char(string="Name Arabic")
    street_arabic = fields.Char(string="Street")
    street2_arabic = fields.Char(string="Street 2")
    city_arabic = fields.Char(string="City")
    state_arabic = fields.Char(string="State")
    zip_arabic = fields.Char(string="Zip")
    country_arabic = fields.Char(string="Country")
