from odoo import fields, models


class PaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    require_install_date = fields.Boolean(string="Require Installation Date")
