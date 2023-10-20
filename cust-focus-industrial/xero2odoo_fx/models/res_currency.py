from odoo import api, fields, models
from odoo.exceptions import UserError


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        if self.env.context.get('force_fx_rate'):
            fx_rate = self.env.context.get('force_fx_rate')
        elif hasattr(self.env.context, 'force_fx_rate'):
            fx_rate = self.env.context.force_fx_rate
        else:
            return super()._get_conversion_rate(from_currency, to_currency, company, date)

        if from_currency == company.currency_id:
            return 1.0 / fx_rate
        elif to_currency == company.currency_id:
            return fx_rate
        else:
            raise UserError("A forced currency rate must be from or to the company currency. {} -> {}".format(
                from_currency.code,
                to_currency.code,
            ))
