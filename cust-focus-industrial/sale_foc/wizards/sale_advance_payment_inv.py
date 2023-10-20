from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    # MIG: 15.0 Function hook
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        for order in sale_orders.filtered(lambda p: p.payment_term_id and p.payment_term_id.require_install_date):
            if not order.install_date:
                raise ValidationError(_(
                    "Order %s requires Installation Date to be set before creating invoices") % order.name)
        return super(SaleAdvancePaymentInv, self).create_invoices()
