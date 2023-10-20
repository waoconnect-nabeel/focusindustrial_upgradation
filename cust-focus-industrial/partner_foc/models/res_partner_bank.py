from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner.bank'

    _sql_constraints = [
        # Add partner_id to the unique constraint to allow two employees at DIFFERENT banks to have the same account number.
        ('unique_number', 'unique(sanitized_acc_number, company_id, partner_id)', 'Account Number must be unique'),
    ]
