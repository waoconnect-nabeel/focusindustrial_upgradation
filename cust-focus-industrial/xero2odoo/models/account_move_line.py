from odoo import api, fields, models, tools


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    force_fx_rate = fields.Float(store=True)  # TODO: should this field be cleared in Odoo if the invoice date is changed?

    @api.depends('currency_id', 'company_id', 'move_id.date')
    def _compute_currency_rate(self):
        self_forced = self.filtered(lambda x: x.force_fx_rate or x.move_id.force_fx_rate)

        for line in self_forced:
            line.currency_rate = line.force_fx_rate or line.move_id.force_fx_rate

        super(AccountMoveLine, self - self_forced)._compute_currency_rate()

    @api.depends('display_type', 'company_id')
    def _compute_account_id(self):
        if self.env.context.get('olaunch_import'):
            # Odoo will trigger an account_id recompute during import and reset what we have imported
            #  This is triggered from account.move:_inverse_partner_id() -> account.move.line:_inverse_partner_id() -> adds compute todo -> account.move.line:_compute_account_id()
            self_super = self - self.filtered(lambda x: x.display_type == 'product' and x.account_id)
            super(AccountMoveLine, self_super)._compute_account_id()
        else:
            super(AccountMoveLine, self)._compute_account_id()

    def _prepare_exchange_difference_move_vals(self, amounts_list, company=None, exchange_date=None):
        vals = super(AccountMoveLine, self)._prepare_exchange_difference_move_vals(
            amounts_list,
            company=company,
            exchange_date=exchange_date,
        )

        # Xero uses the payment date for the exchange differance and Odoo uses the invoice date.
        # To ensure the system matches Xero use the payment date for the exchange date
        #   - We can't use set exchange_date here as super will get the max date and ignore what we put in if its not the latest date
        #   - We will change it on the returned data and set it to the value that was forced
        if self.env.context.get('force_fx_diff_date'):
            vals['move_vals']['date'] = self.env.context['force_fx_diff_date']

        return vals

    def _prepare_reconciliation_single_partial(self, debit_vals, credit_vals):
        return super(AccountMoveLine, self.with_context(
            force_fx_diff_date=debit_vals['record'].move_id.payment_id.force_fx_diff_date or credit_vals['record'].move_id.payment_id.force_fx_diff_date,
        ))._prepare_reconciliation_single_partial(debit_vals, credit_vals)
