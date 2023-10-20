# from odoo import api, fields, models
#
#
# class AccountPaymentRegister(models.TransientModel):
#     _inherit = 'account.payment.register'
#
#     force_fx_rate = fields.Float(store=True)
#     force_fx_diff_date = fields.Date(string="Force the date of any created FX gain/loss journal entry")
#
#     def _create_payments(self):
#         self = self.with_context(default_force_fx_rate=self.force_fx_rate)
#         return super(AccountPaymentRegister, self)._create_payments()
