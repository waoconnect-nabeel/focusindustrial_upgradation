from odoo import fields, models


class FSMPerson(models.Model):
    _name = "fsm.person"
    _inherit = ["fsm.person","mail.thread"]

    color = fields.Integer("Color Index", default=0)
