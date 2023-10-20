from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def reconcile(self):
        return super(AccountMoveLine, self.filtered(lambda aml: aml.credit or aml.debit)).reconcile()
