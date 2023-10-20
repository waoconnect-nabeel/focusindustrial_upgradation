from odoo import api, fields, models
from odoo.osv import expression


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    vendor_ids = fields.Many2many(comodel_name='res.partner')
    use_vendor_pricelists = fields.Boolean(string="Use Vendor Pricelists")
    # MIG: 15.0 Function hook
    def _get_exhausted_inventory_lines_vals(self, non_exhausted_set):
        self.ensure_one()
        if self.vendor_ids:
            vendor_pricelists = self.env['product.supplierinfo'].search([('name','in',self.vendor_ids.mapped('name'))])
            product_ids = vendor_pricelists.mapped('product_tmpl_id.product_variant_id').ids
        else:
            return super(StockInventory, self)._get_exhausted_inventory_lines_vals(non_exhausted_set)

        if self.location_ids:
            location_ids = self.location_ids.ids
        else:
            location_ids = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)]).lot_stock_id.ids

        vals = []
        for product_id in product_ids:
            for location_id in location_ids:
                if ((product_id, location_id) not in non_exhausted_set):
                    vals.append({
                        'inventory_id': self.id,
                        'product_id': product_id,
                        'location_id': location_id,
                        'theoretical_qty': 0
                    })
        return vals
    # MIG: 15.0 Function hook
    def _get_quantities(self):
        self.ensure_one()

        if self.location_ids:
            domain_loc = [('id', 'child_of', self.location_ids.ids)]
        else:
            domain_loc = [('company_id', '=', self.company_id.id), ('usage', 'in', ['internal', 'transit'])]
        locations_ids = [l['id'] for l in self.env['stock.location'].search_read(domain_loc, ['id'])]

        domain = [('company_id', '=', self.company_id.id),
                  ('quantity', '!=', '0'),
                  ('location_id', 'in', locations_ids)]
        if self.prefill_counted_quantity == 'zero':
            domain.append(('product_id.active', '=', True))

        if self.vendor_ids:
            vendor_pricelists = self.env['product.supplierinfo'].search(
                [('name', 'in', self.vendor_ids.mapped('name'))])
            product_ids = vendor_pricelists.mapped('product_tmpl_id.product_variant_id')
            domain = expression.AND([domain, [('product_id', 'in', product_ids.ids)]])
        else:
            return super(StockInventory, self)._get_quantities()

        fields = ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id', 'quantity:sum']
        group_by = ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id']

        quants = self.env['stock.quant'].read_group(domain, fields, group_by, lazy=False)
        return {(
            quant['product_id'] and quant['product_id'][0] or False,
            quant['location_id'] and quant['location_id'][0] or False,
            quant['lot_id'] and quant['lot_id'][0] or False,
            quant['package_id'] and quant['package_id'][0] or False,
            quant['owner_id'] and quant['owner_id'][0] or False):
            quant['quantity'] for quant in quants
        }
