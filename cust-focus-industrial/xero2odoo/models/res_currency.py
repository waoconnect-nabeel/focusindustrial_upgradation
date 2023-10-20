from odoo import api, fields, models


class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        if self.env.context.get('force_fx_rate'):
            return self.env.context['force_fx_rate']

        res = super()._get_conversion_rate(from_currency, to_currency, company, date)
        return res
