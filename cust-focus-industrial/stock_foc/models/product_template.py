from calendar import monthrange

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('internal_reference_uniq', 'UNIQUE (default_code)', 'This internal reference already exists!')
    ]

    def next_6_months_forecast(self):
        self.ensure_one()

        def get_qty_at_date(product, date):
            res = {}
            variants = product.product_variant_ids
            domain_quant_loc, domain_move_in_loc, domain_move_out_loc = variants._get_domain_locations()
            rounding = product.uom_id.rounding
            Move = self.env['stock.move']

            domain_move_in = [('date', '<=', date), ('product_id', 'in', variants.ids)] + domain_move_in_loc
            domain_move_out = [('date', '<=', date), ('product_id', 'in', variants.ids)] + domain_move_out_loc
            domain_move_in_todo = [('state', 'in',
                                    ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
            domain_move_out_todo = [('state', 'in',
                                     ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out

            moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
                                Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'],
                                                orderby='id'))
            moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
                                 Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'],
                                                 orderby='id'))

            for variant in variants:
                qty_available = variant.with_context({'to_date': date}).qty_available
                res[variant.id] = {}
                res[variant.id]['incoming'] = float_round(moves_in_res.get(variant.id, 0.0),
                                                          precision_rounding=rounding)
                res[variant.id]['outgoing'] = float_round(moves_out_res.get(variant.id, 0.0),
                                                          precision_rounding=rounding)
                res[variant.id]['virtual_available'] = float_round(
                    qty_available + res[variant.id]['incoming'] - res[variant.id]['outgoing'],
                    precision_rounding=rounding)

            return sum([res[key]['virtual_available'] for key in res.keys()])

        today = fields.Date.context_today(self)
        month_data = []
        for i in range(6):
            next_month = today + relativedelta(months=i)
            end_of_month = next_month.replace(day=monthrange(next_month.year, next_month.month)[1])
            month_data.append({
                'qty': get_qty_at_date(self, end_of_month),
                'uom': self.uom_id.name,
            })
        return month_data

    def get_next_6_months(self):
        today = fields.Date.context_today(self)
        months = []
        for i in range(6):
            next_month = today + relativedelta(months=i)
            end_of_month = next_month.replace(day=monthrange(next_month.year, next_month.month)[1])
            months.append(end_of_month.strftime('%b'))
        return months
