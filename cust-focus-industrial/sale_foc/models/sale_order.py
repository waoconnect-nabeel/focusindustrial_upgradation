from odoo import api, fields, models
from odoo.tools import float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    install_date = fields.Datetime(string="Installation Date")
    valid_for_days = fields.Char(compute='_compute_valid_for_days')
    delivery_lead_time = fields.Char(string='Delivery Lead Time')
    primary_sales_order = fields.Boolean(string='Primary Sales/ Quotation Order')

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get('install_date'):
            for order in self.filtered(lambda o: o.picking_ids):
                picking_ids = order.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel'])
                picking_ids.write({
                    'scheduled_date': order.install_date,
                })
        for record in self:
            opportunity_id = record.opportunity_id
            #     Set All other sales orders to non=primary sales order
            if vals.get('primary_sales_order') and opportunity_id:
                other_order_ids = opportunity_id.order_ids.filtered(lambda x: x.id != record.id)
                other_order_ids.write({
                    'primary_sales_order': False,
                })
            #     Set Expected Revenue on opportunity
            order_ids = opportunity_id.order_ids.filtered(lambda x: x.state != 'cancel')
            confirmed_order_ids = order_ids.filtered(lambda y: y.state == 'sale')
            primary_order_id = order_ids.filtered(lambda z: z.primary_sales_order)
            recent_order_id = sorted(order_ids, key=lambda x: x.create_date, reverse=True)[:1]
            if confirmed_order_ids and float_compare(sum(confirmed_order_ids.mapped('amount_untaxed')), opportunity_id.expected_revenue, 2):
                opportunity_id.write({
                    'expected_revenue': sum(confirmed_order_ids.mapped('amount_untaxed'))
                })
            elif primary_order_id and float_compare(primary_order_id.amount_untaxed, opportunity_id.expected_revenue, 2):
                opportunity_id.write({
                    'expected_revenue': primary_order_id.amount_untaxed,
                })
            elif recent_order_id and float_compare(recent_order_id[0].amount_untaxed, opportunity_id.expected_revenue, 2):
                opportunity_id.write({
                    'expected_revenue': recent_order_id[0].amount_untaxed,
                })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleOrder, self).create(vals_list)
        for record in res:
            opportunity_id = record.opportunity_id
            #     Set All other sales orders to non=primary sales order
            if record.primary_sales_order and opportunity_id:
                other_order_ids = opportunity_id.order_ids.filtered(lambda x: x.id != record.id)
                other_order_ids.write({
                    'primary_sales_order': False,
                })
            #     Set Expected Revenue on opportunity
            order_ids = opportunity_id.order_ids.filtered(lambda x: x.state != 'cancel')
            confirmed_order_ids = order_ids.filtered(lambda y: y.state == 'sale')
            primary_order_id = order_ids.filtered(lambda z: z.primary_sales_order)
            recent_order_id = sorted(order_ids, key=lambda x: x.create_date, reverse=True)[:1]
            if confirmed_order_ids and float_compare(sum(confirmed_order_ids.mapped('amount_untaxed')), opportunity_id.expected_revenue, 2):
                opportunity_id.write({
                    'expected_revenue': sum(confirmed_order_ids.mapped('amount_untaxed'))
                })
            elif primary_order_id and float_compare(primary_order_id.amount_untaxed, opportunity_id.expected_revenue, 2):
                opportunity_id.write({
                    'expected_revenue': primary_order_id.amount_untaxed,
                })
            elif recent_order_id and float_compare(recent_order_id[0].amount_untaxed, opportunity_id.expected_revenue, 2):
                opportunity_id.write({
                    'expected_revenue': recent_order_id[0].amount_untaxed,
                })
        return res

    def _compute_valid_for_days(self):
        for rec in self:
            if rec.validity_date and rec.date_order:
                valid_for_days = rec.validity_date - fields.Date.context_today(self, rec.date_order)
                rec.valid_for_days = str(valid_for_days).split(',')[0]
            else:
                rec.valid_for_days = False
