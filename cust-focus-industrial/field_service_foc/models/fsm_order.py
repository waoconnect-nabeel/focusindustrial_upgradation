from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    display_name = fields.Char(related=None, compute="compute_display_name", string="Display Name", store=True)

    needs_repair = fields.Boolean("Needs Repair", default=False)
    system_leaks = fields.Boolean("System Leaks", default=False)
    service_interval = fields.Integer("Service Interval __ months")
    other_compressors = fields.Char("Other Compressors")
    test_field = fields.Char(string="Test")

    current_hours = fields.Integer("Current Hours")
    load_hours = fields.Integer("Load Hours")
    load_pressure = fields.Float("Load Pressure")
    unload_load_pressure = fields.Float("Unload Load Pressure")
    operating_temperature = fields.Integer("Operating Temperature")
    compression_temperature = fields.Integer("Ambient Temperature at Compression")

    current_hours_str = fields.Char(compute="_compute_current_hours_str", inverse="_inverse_current_hours_str")
    load_hours_str = fields.Char(compute="_compute_load_hours_str", inverse="_inverse_load_hours_str")
    load_pressure_str = fields.Char(compute="_compute_load_pressure_str", inverse="_inverse_load_pressure_str")
    unload_load_pressure_str = fields.Char(compute="_compute_unload_load_pressure_str", inverse="_inverse_unload_load_pressure_str")
    operating_temperature_str = fields.Char(compute="_compute_operating_temperature_str", inverse="_inverse_operating_temperature_str")
    compression_temperature_str = fields.Char(compute="_compute_compression_temperature_str", inverse="_inverse_compression_temperature_str")

    report_render = fields.Html(compute='compute_report_render')

    technician_signature = fields.Binary("Technician Signature")
    customer_signature = fields.Binary("Customer Signature")

    before_photos = fields.Many2many('ir.attachment', 'fsm_order_before_photo_attachment_rel', 'fsm_order_id',
                                      'attachment_id', 'Before Photos')
    after_photos = fields.Many2many('ir.attachment', 'fsm_order_after_photo_attachment_rel', 'fsm_order_id',
                                      'attachment_id', 'After Photos')

    equipment_lot_name = fields.Char(string="Equipment Serial #", compute='_compute_equipment_lot_name', inverse='_inverse_equipment_lot_name', store=True)
    equipment_lot_id = fields.Many2one("stock.production.lot", string="Equipment Lot",
                                       compute='_compute_equipment_lot_name', store=True)

    notes = fields.Char(string="Important Notes")


    owner_id = fields.Many2one('res.partner', related='location_id.owner_id')
    contact_id = fields.Many2one('res.partner', related='location_id.contact_id')

    region_id = fields.Many2one(readonly=False)
    color = fields.Integer(related="person_id.color", readonly=False)

    display_address = fields.Char(compute="_compute_address")
    default_code = fields.Char(compute="_compute_default_code")

    customer_note_ids = fields.Many2many('fsm.note', compute="_compute_customer_note_ids")

    def _compute_customer_note_ids(self):
        for record in self:
            record.customer_note_ids = record.location_id.notes_ids

    def _compute_default_code(self):
        for record in self:
            record.default_code = ', '.join(record.equipment_ids.filtered(lambda x: x.product_id.default_code).mapped('product_id.default_code'))

    def _compute_current_hours_str(self):
        for rec in self:
            rec.current_hours_str = str(rec.current_hours) if rec.current_hours else False

    def _compute_load_hours_str(self):
        for rec in self:
            rec.load_hours_str = str(rec.load_hours) if rec.load_hours else False

    def _compute_load_pressure_str(self):
        for rec in self:
            rec.load_pressure_str = str(rec.load_pressure) if rec.load_pressure else False

    def _compute_unload_load_pressure_str(self):
        for rec in self:
            rec.unload_load_pressure_str = str(rec.unload_load_pressure) if rec.unload_load_pressure else False

    def _compute_operating_temperature_str(self):
        for rec in self:
            rec.operating_temperature_str = str(rec.operating_temperature) if rec.operating_temperature else False

    def _compute_compression_temperature_str(self):
        for rec in self:
            rec.compression_temperature_str = str(rec.compression_temperature) if rec.compression_temperature else False

    def _inverse_current_hours_str(self):
        for rec in self:
            rec.current_hours = int(rec.current_hours_str) if rec.current_hours_str else False

    def _inverse_load_hours_str(self):
        for rec in self:
            rec.load_hours = int(rec.load_hours_str) if rec.load_hours_str else False

    def _inverse_load_pressure_str(self):
        for rec in self:
            rec.load_pressure = float(rec.load_pressure_str) if rec.load_pressure_str else False

    def _inverse_unload_load_pressure_str(self):
        for rec in self:
            rec.unload_load_pressure = float(rec.unload_load_pressure_str) if rec.unload_load_pressure_str else False

    def _inverse_operating_temperature_str(self):
        for rec in self:
            rec.operating_temperature = int(rec.operating_temperature_str) if rec.operating_temperature_str else False

    def _inverse_compression_temperature_str(self):
            for rec in self:
                rec.compression_temperature = int(rec.compression_temperature_str) if rec.compression_temperature_str else False

    def action_complete(self):
        for rec in self:
            if not rec.technician_signature or not rec.customer_signature:
                raise ValidationError(_("Signatures are required to complete this service"))
            if not rec.equipment_ids or not any(equipment.lot_id and "please enter" not in equipment.lot_id.name.lower() for equipment in rec.equipment_ids):
                raise ValidationError(_("Invalid equipment: order requires at least one equipment with a valid serial number"))
        res = super(FSMOrder, self).action_complete()
        fields = ['needs_repair','system_leaks','service_interval','other_compressors']
        to_do_activity = self.env.ref('mail.mail_activity_data_todo')
        fsm_order_model_id = self.env['ir.model'].search([('model', '=', self._name)], limit=1).id
        for rec in self:
            for field in fields:
                if rec[field]:
                    field_name = rec._fields[field].string

                    self.env['mail.activity'].create({
                        'activity_type_id': to_do_activity.id,
                        'user_id': rec.person_id.user_id.id,
                        'res_id': rec.id,
                        'res_model_id': fsm_order_model_id,
                        'summary': '%s: %s' % (rec.name, field_name),
                    })

        return res

    def compute_report_render(self):
        for rec in self:
            rec.report_render = self.env['ir.qweb']._render('field_service_foc.report_maintenance_report_document', values={'doc': rec, 'disable_render_signature_section': True})

    @api.depends(
        'name',
        'location_id.complete_name',
        'test_field'
    )
    def compute_display_name(self):
        for rec in self:
            rec.display_name = "{} - {}".format(
                rec.location_id.complete_name,
                rec.name,
            )

    def get_extra_task_table(self):
        cols = 4
        activities = self.order_activity_ids.filtered( lambda a: a.state in ['done','todo'])
        rows = '<tr>' if activities else ''
        tot_rows, extra_tds = divmod(len(activities),cols)
        for i,act in enumerate(activities):
            if i > 0 and i % 4 == 0:
                rows += '</tr><tr>'
            icon = '<i style="float:right;font-size:1.3em" class="text-right fa fa-square-o"/>' if act.state == 'todo' else '<i style="float:right;font-size:1.3em" class="text-right fa fa-check-square-o"/>'
            rows += '<td>%s%s</td>' % (act.display_name, icon)

        if rows:
            rows += '<td></td>'* (cols - extra_tds)
            rows += '</tr>'

        return rows

    def get_address(self):
        fields = [i for i in [self.street, self.street2, self.city,self.zip] if i]
        return ', '.join(fields)


    def _compute_address(self):
        for record in self:
            record.display_address = record.get_address()

    @api.onchange("template_id")
    def _onchange_template_id(self):
        if self.template_id:
            self.stock_request_ids = self.template_id.stock_request_ids
        return super(FSMOrder, self)._onchange_template_id()

    def write(self, vals):
        original_scheduled_date_starts = self.read(fields=['scheduled_date_start'])
        res = super(FSMOrder, self).write(vals)
        if not self.env.context.get('updating_recurring_start_date'):
            self.with_context(updating_recurring_start_date=True).update_scheduled_date_on_future_orders(original_scheduled_date_starts)
        return res

    def update_scheduled_date_on_future_orders(self, original_scheduled_date_starts):
        if not original_scheduled_date_starts:
            return
        original_scheduled_date_starts = {x['id']: x['scheduled_date_start'] for x in original_scheduled_date_starts}
        for rec in self:
            if not rec.scheduled_date_start or not rec.fsm_recurring_id:
                continue
            original_scheduled_date_start = original_scheduled_date_starts[rec.id]
            date_changed_by_timespan = (rec.scheduled_date_start - original_scheduled_date_start)

            future_orders = rec.fsm_recurring_id.fsm_order_ids.filtered(lambda f: f.scheduled_date_start > rec.scheduled_date_start and not f.stage_id.is_closed)
            for future_order in future_orders:
                future_order.scheduled_date_start += date_changed_by_timespan

    @api.depends('equipment_ids')
    def _compute_equipment_lot_name(self):
        for rec in self:
            if rec.equipment_ids.filtered(lambda x: x.lot_id):
                rec.equipment_lot_name = rec.equipment_ids.filtered(lambda x: x.lot_id)[0].lot_id.name
                rec.equipment_lot_id = rec.equipment_ids.filtered(lambda x: x.lot_id)[0].lot_id
            else:
                rec.equipment_lot_name = False
                rec.equipment_lot_id = False

    def _inverse_equipment_lot_name(self):
        for rec in self:
            if rec.equipment_ids.filtered(lambda x: x.lot_id):
                rec.equipment_ids.filtered(lambda x: x.lot_id)[0].lot_id.name = rec.equipment_lot_name

    def open_map(self):
        self.ensure_one()
        url = "http://maps.google.com/maps?oi=map&q="
        if self.street:
            url += self.street.replace(' ', '+')
        if self.city:
            url += '+' + self.city.replace(' ', '+')
        if self.state_name:
            url += '+' + self.state_name.replace(' ', '+')
        if self.country_name:
            url += '+' + self.country_name.replace(' ', '+')
        if self.zip:
            url += '+' + self.zip.replace(' ', '+')
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new'
        }

    def set_to_be_scheduled(self):
        if self.stage_id == self.env.ref('fieldservice.fsm_stage_new'):
            self.stage_id = self.env['fsm.stage'].browse(7)  # Scheduled
