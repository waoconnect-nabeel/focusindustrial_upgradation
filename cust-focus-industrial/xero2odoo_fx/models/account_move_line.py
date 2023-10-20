from odoo import api, fields, models, tools


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    force_fx_rate = fields.Float(store=True)  # TODO: should this field be cleared in Odoo if the invoice date is changed?

    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        force_fx_rate = self.force_fx_rate or self.move_id.force_fx_rate
        self = self.with_context(force_fx_rate=force_fx_rate)
        currency = currency.with_context(force_fx_rate=force_fx_rate)
        return super(AccountMoveLine, self)._get_fields_onchange_subtotal_model(price_subtotal, move_type, currency, company, date)

    @api.onchange('amount_currency')
    def _onchange_amount_currency(self):
        # We are doing this as a hack since you can't change the context of self on an onchange.
        self.env.context.force_fx_rate = self.force_fx_rate
        return super()._onchange_amount_currency()

    def reconcile(self):
        force_fx_rate = list(set(self.filtered(lambda x: x.force_fx_rate).mapped('force_fx_rate')))
        if len(force_fx_rate) > 1:
            raise UserWarning("You can not reconcile a stock move that has multiple forced fx rates")
        force_fx_rate = force_fx_rate[0] if force_fx_rate else False

        self = self.with_context(force_fx_rate=force_fx_rate)
        return super(AccountMoveLine, self).reconcile()

    @api.depends('purchase_line_id.qty_received', 'purchase_line_id.qty_invoiced', 'purchase_line_id.product_qty')
    def _can_be_paid(self):
        for rec in self:
            super(AccountMoveLine, rec.with_context(
                force_fx_rate=rec.force_fx_rate or rec.move_id.force_fx_rate,
            ))._can_be_paid()
