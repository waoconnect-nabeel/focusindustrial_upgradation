from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name_clean = fields.Text(compute="_compute_name_clean")

    def _compute_name_clean(self):
        for line in self:
            if line.name and line.product_id.default_code and line.product_id.default_code in line.name:
                line.name_clean = line.name.split(line.product_id.default_code)[-1].strip(']').strip(' -')
            else:
                line.name_clean = line.name

    # MIG: 15.0 Function hook
    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        values.update({
            'install_date': self.order_id.install_date or False,
        })
        return values
