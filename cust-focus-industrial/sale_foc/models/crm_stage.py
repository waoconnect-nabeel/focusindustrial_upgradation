from odoo import api, fields, models
from odoo.tools import float_compare


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    is_qualified_stage = fields.Boolean()
