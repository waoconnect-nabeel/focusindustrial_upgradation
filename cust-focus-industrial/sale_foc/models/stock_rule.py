from odoo import api, fields, models


class StockRule(models.Model):
    _inherit = 'stock.rule'
    # MIG: 15.0 Function hook
    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        res = super(StockRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        if values.get('install_date'):
            res['date'] = values.get('install_date')
        return res
