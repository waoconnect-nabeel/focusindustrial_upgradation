from odoo import api, fields, models


class FSMEquipment(models.Model):
    _inherit = "fsm.equipment"

    equipment_make = fields.Char("Make")
    equipment_model = fields.Char("Model")
    equipment_type = fields.Char("type")
