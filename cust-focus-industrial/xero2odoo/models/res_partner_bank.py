from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner.bank'

    _sql_constraints = [
        # TODO: Work out if this can be fixed in Odoo Online (ir.model.constraint?)
        # Add partner_id to the unique constraint to allow two employees at DIFFERENT banks to have the same account number.
        #   It's not their fault if a bank re-uses the same account number with a different bsb number...
        ('unique_number', 'unique(sanitized_acc_number, company_id, partner_id)', 'Account Number must be unique'),
    ]
