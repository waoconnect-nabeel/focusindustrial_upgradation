import datetime

from odoo import fields, models


class FSMNote(models.Model):

    _name = "fsm.note"
    _description = "Field Service Note"
    _order = "date desc"

    note = fields.Text(readonly=False, required=True)
    date = fields.Date(string='Date', required=True, default=lambda self: fields.Date.context_today(self))
    customer_id = fields.Many2one(
        "fsm.location", string="Customer", index=True, required=True
    )
