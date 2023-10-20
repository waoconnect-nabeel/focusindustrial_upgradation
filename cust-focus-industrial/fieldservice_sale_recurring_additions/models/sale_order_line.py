from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends("product_id")
    def _compute_qty_delivered_method(self):
        super(SaleOrderLine, self)._compute_qty_delivered_method()
        for line in self:
            if not line.is_expense and line.product_id.field_service_tracking == "recurring":
                line.qty_delivered_method = "field_service"


    @api.depends("fsm_recurring_id.fsm_order_ids.stage_id")
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()
        lines_by_fsm = self.filtered(
            lambda sol: sol.qty_delivered_method == "field_service"
        )
        complete = self.env.ref("fieldservice.fsm_stage_completed")
        for line in lines_by_fsm:
            fsm_orders = line.fsm_recurring_id.fsm_order_ids.filtered(lambda fsm_order: fsm_order.stage_id == complete)
            qty = len(fsm_orders)
            line.qty_delivered = qty
