from odoo import fields, models


class FSMTemplate(models.Model):
    _inherit = "fsm.template"

    stock_request_ids = fields.Many2many(string="Inventory", comodel_name="stock.request")
