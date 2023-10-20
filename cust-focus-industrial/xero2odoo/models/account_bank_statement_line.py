from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    force_fx_rate = fields.Float(store=True)

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        return super(AccountBankStatementLine, self.with_context(
            force_fx_rate=self.force_fx_rate,
        ))._prepare_move_line_default_vals(counterpart_account_id=counterpart_account_id)

    def _get_amounts_with_currencies(self):
        return super(AccountBankStatementLine, self.with_context(
            force_fx_rate=self.force_fx_rate,
        ))._get_amounts_with_currencies()
