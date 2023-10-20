from odoo import api, fields, models


class ResPartnerNote(models.Model):
    _name = 'res.partner.note'
    _description = "Partner Notes"

    note = fields.Text()
    partner_id = fields.Many2one('res.partner')
