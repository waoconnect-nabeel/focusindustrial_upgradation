from odoo import api, fields, models


class FsmRecurringTemplate(models.Model):
    _inherit = 'fsm.recurring.template'

    start_offset_months = fields.Integer()
    auto_confirm_orders = fields.Boolean(default=True)

    fsm_order_template_odd_position_id = fields.Many2one('fsm.template', string="Order template (Even)")
    fsm_order_template_even_position_id = fields.Many2one('fsm.template', string="Order template (Odd)")
