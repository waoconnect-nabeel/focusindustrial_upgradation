from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange(
        'force_fx_rate',
    )
    def _onchange_force_fx_rate(self):
        self._onchange_currency()

    def _post(self, soft=True):
        has_force_fx = any([True for x in self if x.force_fx_rate])
        if not has_force_fx:
            return super()._post()

        if len(self) > 1:
            raise UserError('Only one record can be processed at a time when an fx rate is forced (_post)')

        force_fx_rate = self.force_fx_rate
        self = self.with_context(force_fx_rate=force_fx_rate)
        return super(AccountMove, self)._post(soft=soft)

    def _compute_invoice_taxes_by_group(self):
        has_force_fx = any([True for x in self if x.force_fx_rate])
        if not has_force_fx:
            return super()._compute_invoice_taxes_by_group()

        if len(self) > 1:
            raise UserError('Only one record can be processed at a time when an fx rate is forced (_compute_invoice_taxes_by_group)')

        force_fx_rate = self.force_fx_rate
        self = self.with_context(force_fx_rate=force_fx_rate)
        return super(AccountMove, self)._compute_invoice_taxes_by_group()

    def _recompute_tax_lines(self, recompute_tax_base_amount=False, tax_rep_lines_to_recompute=None):
        has_force_fx = any([True for x in self if x.force_fx_rate])
        if not has_force_fx:
            return super()._recompute_tax_lines()

        if len(self) > 1:
            raise UserError('Only one record can be processed at a time when an fx rate is forced (_recompute_tax_lines)')

        force_fx_rate = self.force_fx_rate
        self = self.with_context(force_fx_rate=force_fx_rate)
        return super(AccountMove, self)._recompute_tax_lines(recompute_tax_base_amount=recompute_tax_base_amount)

    def reconcile(self):
        has_force_fx = any([True for x in self if x.force_fx_rate])
        if not has_force_fx:
            return super().reconcile()

        if len(self) > 1:
            raise UserError('Only one record can be processed at a time when an fx rate is forced (reconcile)')

        force_fx_rate = self.force_fx_rate
        self = self.with_context(force_fx_rate=force_fx_rate)
        return super(AccountMove, self).reconcile()
