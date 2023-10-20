from odoo import api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    force_fx_rate = fields.Float(store=True)

    def button_validate(self):
        has_force_fx = any([True for x in self if x.force_fx_rate])
        if not has_force_fx:
            return super().button_validate()

        if len(self) > 1:
            raise UserError('You must complete deliveries one at a time if there is a forced fx rate')

        return super(StockPicking, self.with_context(
            force_fx_rate=self.force_fx_rate or self.purchase_id.force_fx_rate,
        )).button_validate()


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    force_fx_rate = fields.Float(store=True)

    def button_confirm(self):
        for rec in self:
            super(PurchaseOrder, rec.with_context(
                force_fx_rate=rec.force_fx_rate,
            )).button_confirm()
        return True


    def _create_picking(self):
        for rec in self:
            super(PurchaseOrder, rec.with_context(
                force_fx_rate=rec.force_fx_rate,
            ))._create_picking()
        return True
