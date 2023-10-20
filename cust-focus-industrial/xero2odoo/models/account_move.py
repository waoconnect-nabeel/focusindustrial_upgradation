from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    force_fx_rate = fields.Float(store=True)

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        if self.env.context.get('olaunch_import'):
            self_need_name = self.filtered(lambda x: not x.name or x.name == '/')
            if self_need_name:
                super(AccountMove, self_need_name)._compute_name()
            self._compute_split_sequence()
        else:
            super(AccountMove, self)._compute_name()
