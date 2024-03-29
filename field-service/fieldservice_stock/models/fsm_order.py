# Copyright (C) 2021 - TODAY, Brian McMaster
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

REQUEST_STATES = [
    ("draft", "Draft"),
    ("submitted", "Submitted"),
    ("open", "In progress"),
    ("done", "Done"),
    ("cancel", "Cancelled"),
]


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env["stock.warehouse"].search(
            [("company_id", "=", company)], limit=1
        )
        return warehouse_ids and warehouse_ids.id

    @api.model
    def _get_move_domain(self):
        return [("picking_id.picking_type_id.code", "in", ("outgoing", "incoming"))]

    stock_request_ids = fields.One2many(
        "stock.request", "fsm_order_id", string="Order Lines"
    )

    picking_ids = fields.One2many("stock.picking", "fsm_order_id", string="Transfers")
    delivery_count = fields.Integer(
        string="Delivery Orders", compute="_compute_picking_ids"
    )
    procurement_group_id = fields.Many2one(
        "procurement.group", "Procurement Group", copy=False
    )
    inventory_location_id = fields.Many2one(
        related="location_id.inventory_location_id", readonly=True
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Warehouse",
        required=True,
        default=_default_warehouse_id,
        help="Warehouse used to ship the materials",
    )
    return_count = fields.Integer(
        string="Return Orders", compute="_compute_picking_ids"
    )
    request_stage = fields.Selection(
        REQUEST_STATES,
        string="Request State",
        default="draft",
        readonly=True,
        store=True,
    )
    move_ids = fields.One2many(
        "stock.move", "fsm_order_id", string="Operations", domain=_get_move_domain
    )

    def action_request_submit(self):
        for rec in self:
            if not rec.stock_request_ids:
                raise UserError(_("Please create a stock request."))
            for line in rec.stock_request_ids:
                if line.state == "draft":
                    if line.order_id:
                        line.order_id.action_confirm()
                    else:
                        line.action_submit()
            rec.request_stage = "submitted"

    def action_request_cancel(self):
        for rec in self:
            if not rec.stock_request_ids:
                raise UserError(_("Please create a stock request."))
            for line in rec.stock_request_ids:
                if line.state in ("draft", "submitted"):
                    if line.order_id:
                        line.order_id.action_cancel()
                    else:
                        line.action_cancel()
            rec.request_stage = "cancel"

    def action_request_draft(self):
        for rec in self:
            if not rec.stock_request_ids:
                raise UserError(_("Please create a stock request."))
            for line in rec.stock_request_ids:
                if line.state == "cancel":
                    if line.order_id:
                        line.order_id.action_draft()
                    else:
                        line.action_draft()
            rec.request_stage = "draft"

    @api.depends("picking_ids")
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(
                [
                    picking
                    for picking in order.picking_ids
                    if picking.picking_type_id.code == "outgoing"
                ]
            )
            order.return_count = len(
                [
                    picking
                    for picking in order.picking_ids
                    if picking.picking_type_id.code == "incoming"
                ]
            )

    def action_view_delivery(self):
        """
        This function returns an action that display existing delivery orders
        of given fsm order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        """
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        pickings = self.mapped("picking_ids")
        delivery_ids = [
            picking.id
            for picking in pickings
            if picking.picking_type_id.code == "outgoing"
        ]
        if len(delivery_ids) > 1:
            action["domain"] = [("id", "in", delivery_ids)]
        elif pickings:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = delivery_ids[0]
        return action

    def action_view_returns(self):
        """
        This function returns an action that display existing return orders
        of given fsm order ids. It can either be a in a list or in a form
        view, if there is only one return order to show.
        """
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        pickings = self.mapped("picking_ids")
        return_ids = [
            picking.id
            for picking in pickings
            if picking.picking_type_id.code == "incoming"
        ]
        if len(return_ids) > 1:
            action["domain"] = [("id", "in", return_ids)]
        elif pickings:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = return_ids[0]
        return action
