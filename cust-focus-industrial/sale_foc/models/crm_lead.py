from odoo import api, fields, models
from odoo.tools import float_compare


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    has_qualified = fields.Boolean(tracking=True)

    def write(self, vals):
        if vals.get('stage_id') and 'has_qualified' not in vals:
            stage = self.env['crm.stage'].browse(vals['stage_id'])
            if stage.is_qualified_stage:
                vals['has_qualified'] = True
        return super().write(vals)
