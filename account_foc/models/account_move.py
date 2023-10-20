from odoo import api, fields, models

SALES_TYPE_SELECTION = [
    ('service', 'Service'),
    ('reseller', 'Reseller / Dealer'),
    ('direct', 'Direct Sales'),
    ('other', 'Other'),
]


class AccountMove(models.Model):
    _inherit = 'account.move'

    source_type = fields.Selection(string="Source Type", selection=SALES_TYPE_SELECTION, compute="_compute_sales_type", store=True)

    @api.depends('user_id', 'partner_id.category_id')
    def _compute_sales_type(self):
        reseller_tag = self.env.ref('account_foc.reseller_tag', raise_if_not_found=False)
        for rec in self:
            if rec.user_id.has_group('account_foc.group_source_type_service'):
                rec.source_type = 'service'
            elif rec.user_id.has_group('account_foc.group_source_type_other'):
                rec.source_type = 'other'
            elif reseller_tag in rec.partner_id.category_id:
                rec.source_type = 'reseller'
            else:
                rec.source_type = 'direct'
