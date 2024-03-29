# Copyright (C) 2021 Brian McMaster
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    fsm_order_id = fields.Many2one("fsm.order", string="Field Service Order")

    def prepare_equipment_values(self, move_line):
        location = move_line.move_id.stock_request_ids.fsm_order_id.location_id
        return {
            "name": "{} ({})".format(move_line.product_id.name, move_line.lot_id.name),
            "product_id": move_line.product_id.id,
            "lot_id": move_line.lot_id.id,
            "location_id": location.id,
            "current_location_id": location.id,
            "current_stock_location_id": move_line.location_dest_id.id,
        }

    def _action_done(self, cancel_backorder=False):
        res = super()._action_done(cancel_backorder=False)
        for rec in self:
            if (
                rec.state == "done"
                and rec.picking_type_id.create_fsm_equipment
                and rec.product_tmpl_id.create_fsm_equipment
            ):
                for line in rec.move_line_ids:
                    vals = self.prepare_equipment_values(line)
                    line.lot_id.fsm_equipment_id = rec.env["fsm.equipment"].create(vals)
        return res
