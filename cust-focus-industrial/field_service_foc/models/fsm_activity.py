from odoo import api, fields, models


class FsmActivity(models.Model):
    _inherit = 'fsm.activity'

    action_bool_field_cancel = fields.Boolean(compute="compute_action_bool_field_cancel", inverse="inverse_action_bool_field_cancel")
    action_bool_field_complete = fields.Boolean(compute="compute_action_bool_field_complete", inverse="inverse_action_bool_field_complete")

    def compute_action_bool_field_cancel(self):
        for rec in self:
            rec.action_bool_field_cancel = rec.state == 'cancel'

    def compute_action_bool_field_complete(self):
        for rec in self:
            rec.action_bool_field_complete = rec.state == 'done'

    def inverse_action_bool_field_cancel(self):
        for rec in self:
            if rec.action_bool_field_cancel:
                rec.action_cancel()

    def inverse_action_bool_field_complete(self):
        for rec in self:
            if rec.action_bool_field_complete:
                rec.action_done()
