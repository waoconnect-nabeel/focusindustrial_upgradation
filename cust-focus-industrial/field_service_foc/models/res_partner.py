from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    create_fsm_location = fields.Boolean("Create FSM Location")
    fsm_report_count = fields.Integer("FSM Order Count", compute="compute_fsm_report_count")

    @api.constrains('create_fsm_location')
    def _create_fsm_location_for_commercial_partner(self):
        for partner in self.filtered(lambda p: p.create_fsm_location):
            res = self.env["fsm.location"].search_count([("partner_id", "=", partner.id)])
            if res == 0:
                vals = self.env['fsm.wizard']._prepare_fsm_location(partner)
                self.env["fsm.location"].create(vals)
                partner.write({"fsm_location": True})

    def compute_fsm_report_count(self):
        for rec in self:
            rec.fsm_report_count = self.env['fsm.order'].search_count([
                ('location_id.owner_id', 'child_of', rec.id),
            ])

    def action_open_fsm_reports(self):
        for rec in self:
            fsm_reports = self.env["fsm.order"].search([
                ('location_id.owner_id', 'child_of', rec.id),
            ])
            action = self.env.ref("fieldservice.action_fsm_operation_order").read()[0]
            action["context"] = {}
            if len(fsm_reports) > 1:
                action["domain"] = [("id", "in", fsm_reports.ids)]
            elif len(fsm_reports) == 1:
                action["views"] = [
                    (self.env.ref("fieldservice.fsm_order_form").id, "form")
                ]
                action["res_id"] = fsm_reports.ids[0]
            return action
