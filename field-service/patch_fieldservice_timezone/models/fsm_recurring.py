from odoo import api, fields, models


class FsmRecurring(models.Model):
    _inherit = 'fsm.recurring'

    def _prepare_order_values(self, date=None):
        date = fields.Datetime.convert_datetime_to_user_tz(self, date.replace(tzinfo=None)).replace(tzinfo=None)
        return super(FsmRecurring, self)._prepare_order_values(date=date)
