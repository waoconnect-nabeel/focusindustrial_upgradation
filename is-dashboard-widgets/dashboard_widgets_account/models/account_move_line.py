from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    user_type_id = fields.Many2one('account.account.type', related="account_id.user_type_id", store=True)
    amount_residual_negative = fields.Monetary(compute="compute_amount_residual_negative", store=True, string="Amount Due (Negative)")

    @api.depends('amount_residual')
    def compute_amount_residual_negative(self):
        for rec in self:
            rec.amount_residual_negative = -rec.amount_residual
