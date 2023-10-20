from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'
    # MIG: 15.0 Function hook
    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        install_date = self.mapped('sale_line_id.order_id.install_date')
        if install_date:
            vals['scheduled_date'] = install_date[0]
        return vals
