from odoo import api, fields, models

from datetime import datetime
from dateutil.relativedelta import relativedelta


class FsmRecurring(models.Model):
    _inherit = 'fsm.recurring'

    fsm_order_template_odd_position_id = fields.Many2one('fsm.template', string="Order template (Even)")
    fsm_order_template_even_position_id = fields.Many2one('fsm.template', string="Order template (Odd)")

    def action_start(self):
        for rec in self:
            if rec.fsm_recurring_template_id.start_offset_months:
                rec.start_date = datetime.now() + relativedelta(months=rec.fsm_recurring_template_id.start_offset_months)
        if self.env.context.get('creating_fsm'):
            # Only call super for orders that have a template that allows auto confirming
            return super(FsmRecurring, self.filtered(lambda r: r.fsm_recurring_template_id.auto_confirm_orders)).action_start()

        return super(FsmRecurring, self).action_start()

    def populate_from_template(self, template=False):
        vals = super(FsmRecurring, self).populate_from_template(template=template)
        if not template:
            template = self.fsm_recurring_template_id
        vals['fsm_order_template_odd_position_id'] = template.fsm_order_template_odd_position_id
        vals['fsm_order_template_even_position_id'] = template.fsm_order_template_even_position_id
        return vals

    # MIG 15
    def _prepare_order_values(self, date=None):
        template = self.fsm_order_template_id

        order_count = len(self.fsm_order_ids or [])
        if self.fsm_order_template_even_position_id and order_count % 2:  # Even
            template = self.fsm_order_template_even_position_id
        elif self.fsm_order_template_odd_position_id and not order_count % 2:  # Odd
            template = self.fsm_order_template_odd_position_id

        # MIG: Copied from OCA and chagned code to have a template var we can use and only update the dict keys that used template
        res = super(FsmRecurring, self)._prepare_order_values(date=date)
        res["template_id"] = template.id
        res["scheduled_duration"] = template.duration
        res["category_ids"] = [(6, False, template.category_ids.ids)]
        return res
