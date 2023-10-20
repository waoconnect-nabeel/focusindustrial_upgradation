from odoo import api, fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    # MIG: 15.0 Function hook
    def _get_product_context(self):
        """
        standard Odoo uses the product's first vendors lead time as the 'to_date' which means that
        any incoming stock due after that lead time will not be recognised in the forecasted qty on the replenishments.
        FOC want the forecasted qty to match the forecasted qty found on the product form.
        As a result of this, the qty_to_order will be reduced by the forecasted qty.
        """
        res = super(StockWarehouseOrderpoint, self)._get_product_context()
        res.pop('to_date', None)
        return res
