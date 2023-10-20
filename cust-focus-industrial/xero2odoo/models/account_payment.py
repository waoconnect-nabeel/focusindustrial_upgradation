from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    force_fx_rate = fields.Float(store=True)
    force_fx_diff_date = fields.Date(string="Force the date of any created FX gain/loss journal entry")

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        return super(AccountPayment, self.with_context(
            force_fx_rate=self.force_fx_rate,
        ))._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
