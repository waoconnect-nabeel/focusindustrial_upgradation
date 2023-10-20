from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _field_create_fsm_recurring(self):
        return super(SaleOrderLine, self.with_context(creating_fsm=True))._field_create_fsm_recurring()

    def _field_create_fsm_recurring_prepare_values(self):
        res = super(SaleOrderLine, self)._field_create_fsm_recurring_prepare_values()

        template = self.product_id.fsm_recurring_template_id
        res['fsm_order_template_odd_position_id'] = template.fsm_order_template_odd_position_id.id
        res['fsm_order_template_even_position_id'] = template.fsm_order_template_even_position_id.id

        return res
