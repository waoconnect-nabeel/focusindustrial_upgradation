from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fsm_equipment_ids = fields.Many2many('fsm.equipment', string="Equipments", compute='_compute_fsm_equipment_ids')
    fsm_order_ids = fields.One2many('fsm.order', inverse_name='owner_id')
    note_ids = fields.One2many('res.partner.note', inverse_name='partner_id')
    invoice_line_ids = fields.One2many('account.move.line', inverse_name='partner_id', domain=[('move_id.move_type', 'in', ['out_invoice', 'out_refund', 'in_invoice', 'in_refund'])])

    def _compute_fsm_equipment_ids(self):
        def get_locations_equipment(locs):
            equip = self.env['fsm.equipment']
            child_locs = self.env["fsm.location"].search(
                [("fsm_parent_id", "in", locs.ids)]
            )
            equip |= self.env["fsm.equipment"].search(
                [("location_id", "in", locs.ids)]
            )
            if child_locs:
                equip |= get_locations_equipment(child_locs)
            return equip

        for rec in self:
            location_ids = rec.owned_location_ids
            rec.fsm_equipment_ids = get_locations_equipment(location_ids)
