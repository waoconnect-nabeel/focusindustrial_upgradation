from dateutil.rrule import rruleset

from odoo import api, fields, models


class FSMFrequencySet(models.Model):
    _inherit = 'fsm.frequency.set'

    def _get_rruleset(self, dtstart=None, until=None):
        if dtstart:
            dtstart = fields.Datetime.context_timestamp(self, dtstart)
        if until:
            until = fields.Datetime.context_timestamp(self, until)
        return super(FSMFrequencySet, self)._get_rruleset(dtstart, until)
