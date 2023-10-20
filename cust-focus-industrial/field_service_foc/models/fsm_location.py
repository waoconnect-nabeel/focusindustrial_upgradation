from odoo import fields, models


class FSMLocation(models.Model):

    _inherit = "fsm.location"

    notes_ids = fields.One2many(comodel_name="fsm.note", inverse_name="customer_id", string="Customer Notes")
