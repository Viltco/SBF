from odoo import models, fields, api, _
from odoo.exceptions import UserError
import math
from datetime import datetime


class QualityCheckInh(models.Model):
    _inherit = 'quality.check'

    # def action_reset(self):
    #     self.quality_state = 'none'
