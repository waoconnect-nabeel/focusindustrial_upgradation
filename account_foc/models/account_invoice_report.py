from odoo import api, fields, models

from odoo.addons.account_foc.models.account_move import SALES_TYPE_SELECTION


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    source_type = fields.Selection(string="Source Type", selection=SALES_TYPE_SELECTION)

    # MIG: 15.0 Function hook
    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", move.source_type as source_type"
