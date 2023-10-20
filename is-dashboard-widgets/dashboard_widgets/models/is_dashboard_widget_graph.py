from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval as safe_eval



class DashboardWidgetGraph(models.Model):
    _inherit = 'is.dashboard.widget'

    DATE_AGGREGATE_OPERATORS = [
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('quarter', 'Quarter'),
        ('year', 'Year'),
    ]

    display_mode = fields.Selection(selection_add=[
        ('graph', 'Chart / Graph'),
    ], required=True, ondelete={'graph': 'set default'})

    graph_type = fields.Selection(string="Chart Type", selection=[
        ('line', 'Line'),
        ('bar', 'Bar'),
        ('pie', 'Pie'),
        ('radar', 'Radar'),
    ])

    show_values_on_graph = fields.Boolean(string="Show Values on Graph")
    hide_legend = fields.Boolean(string="Hide Legend", default=False)
    use_suggested_min_y_axis = fields.Boolean(string="Set Minimum Y axis Value?", help="Minimum will be this value, unless there is a lower value")
    use_suggested_max_y_axis = fields.Boolean(string="Set Maximum Y axis Value?", help="Maximum will be this value, unless there is a higher value")
    suggested_min_y_axis = fields.Integer(string="Minimum Y Axis value", help="Minimum will be this value, unless there is a lower value")
    suggested_max_y_axis = fields.Integer(string="Maximum Y Axis value", help="Maximum will be this value, unless there is a higher value")
    use_decimal_precision_y_axis = fields.Boolean(string="Set Decimal Precision on Y Axis?", help="This will set the decimal precision on the Y Axis labels")
    decimal_precision_y_axis = fields.Integer(string="Decimal Precision", help="This will set the decimal precision on the Y Axis labels")
    chart_display_value_prefix = fields.Char()

    label_1_regex = fields.Char(string="Label regex (1)", help="Label will be first regex match eg. '\d+' to get first number")
    chart_1_config_show_average_dataset = fields.Boolean(default=False, string="Show Average Dataset (1)")
    chart_1_config_aggregate_field_id = fields.Many2one('ir.model.fields',  string="Chart Group By (1)")
    chart_1_config_aggregate_operator = fields.Selection(string="Chart Group By Operator (1)", selection=DATE_AGGREGATE_OPERATORS, default='month')
    chart_1_config_aggregate_operator_supported = fields.Boolean(string="Chart Group By Operator Supported (1)", compute='compute_chart_1_config_aggregate_operator_supported')
    chart_1_config_aggregate2_field_id = fields.Many2one('ir.model.fields',  string="Chart Group By 2 (1)")
    chart_1_config_aggregate2_operator = fields.Selection(string="Chart Group By Operator 2 (1)", selection=DATE_AGGREGATE_OPERATORS, default='month')
    chart_1_config_aggregate2_operator_supported = fields.Boolean(string="Chart Group By Operator 2 Supported (1)", compute='compute_chart_1_config_aggregate2_operator_supported')
    chart_1_config_show_empty_groups = fields.Boolean("Show Empty Groups (1)")
    chart_1_config_color = fields.Char("Chart Color (1)", default='#4286f4', help="HTML Color code eg. #4286f4")
    chart_1_config_area = fields.Boolean("Chart Show Area (1)")
    chart_1_config_title = fields.Char("Chart Title (1)", default="Query 1")
    chart_1_config_sort_field_id = fields.Many2one('ir.model.fields',  string="Chart Sort By (1)")
    chart_1_config_sort_default_by_label = fields.Boolean(default=True, string="Chart Sort By Group by Label (or value)", help="When no sort column is selected sort by label of group by. Tick to sort by label and untick to sort by value. eg. Selection field value or selection field label")
    chart_1_config_sort_descending = fields.Boolean(string="Chart Sort By Desc. (1)")

    chart_1_goal_config_color = fields.Char("Chart Goal Color (1)")  # default='#839ac1'
    chart_1_goal_config_area = fields.Boolean("Chart Goal Show Area (1)", default=False)
    chart_1_goal_config_title = fields.Char("Chart Goal Title (1)", default="Goal 1")

    label_2_regex = fields.Char(string="Label regex (2)", help="Label will be first regex match eg. '\d+' to get first number")
    chart_2_config_show_average_dataset = fields.Boolean(default=False, string="Show Average Dataset (2)")
    chart_2_config_aggregate_field_id = fields.Many2one('ir.model.fields',  string="Chart Group By (2)")
    chart_2_config_aggregate_operator = fields.Selection(string="Chart Group By Operator (2)", selection=DATE_AGGREGATE_OPERATORS, default='month')
    chart_2_config_aggregate_operator_supported = fields.Boolean(string="Chart Group By Operator Supported (2)", compute='compute_chart_2_config_aggregate_operator_supported')
    chart_2_config_aggregate2_field_id = fields.Many2one('ir.model.fields',  string="Chart Group By 2 (2)")
    chart_2_config_aggregate2_operator = fields.Selection(string="Chart Group By Operator 2 (2)", selection=DATE_AGGREGATE_OPERATORS, default='month')
    chart_2_config_aggregate2_operator_supported = fields.Boolean(string="Chart Group By Operator 2 Supported (2)", compute='compute_chart_2_config_aggregate2_operator_supported')
    chart_2_config_show_empty_groups = fields.Boolean("Show Empty Groups (2)")
    chart_2_config_color = fields.Char("Chart Color (2)")
    chart_2_config_area = fields.Boolean("Chart Show Area (2)")
    chart_2_config_title = fields.Char("Chart Title (2)", default="Query 2")
    chart_2_config_sort_field_id = fields.Many2one('ir.model.fields',  string="Chart Sort By (2)")
    chart_2_config_sort_default_by_label = fields.Boolean(default=True, string="Chart Sort By Group by Label (or value) (2)", help="When no sort column is selected sort by label of group by. Tick to sort by label and untick to sort by value. eg. Selection field value or selection field label")
    chart_2_config_sort_descending = fields.Boolean(string="Chart Sort By Desc. (2)")

    chart_2_goal_config_color = fields.Char("Chart Goal Color (2)")  # default='#8d94a0'
    chart_2_goal_config_area = fields.Boolean("Chart Goal Show Area (2)", default=False)
    chart_2_goal_config_title = fields.Char("Chart Goal Title (2)", default="Goal 2")

    def get_render_data(self):
        render_data = super(DashboardWidgetGraph, self).get_render_data()

        if self.display_mode != 'graph':
            return render_data

        render_data['chart_text_table'] = self.get_chart_text_html()
        return render_data

    def get_chart_text_html(self):
        res = ""
        if self.display_mode == 'graph':
            chart_data = self.get_dashboard_data()
            if not chart_data:
                res = "No data"
            else:
                res += "<table>"
                res += "<thead>"
                res += '<tr>'
                res += '<th>&nbsp;</th>'
                for col in chart_data['data']['labels']:
                    res += '<th style="border-bottom: 1px solid gray;">{}</th>'.format(
                        col,
                    )
                res += "</tr>"
                res += "</thead>"
                res += "<tbody>"

                for i, ds in enumerate(chart_data['data']['datasets']):
                    res += '<tr style="border-bottom: 1px gray;">'
                    ds_label = "{}".format(ds['label']) if len(chart_data['data']['datasets']) > 1 else ""
                    for col in [ds_label] + ds['data']:
                        res += '<td style="border-bottom: 1px solid gray;">{}</td>'.format(
                            col
                        )
                    res += "</tr>"
                res += "</tbody>"
                res += "</table>"
        return res

    @api.depends('chart_1_config_aggregate_field_id')
    def compute_chart_1_config_aggregate_operator_supported(self):
        for rec in self:
            rec.chart_1_config_aggregate_operator_supported = rec.chart_1_config_aggregate_field_id.ttype in ['date', 'datetime']

    @api.depends('chart_2_config_aggregate_field_id')
    def compute_chart_2_config_aggregate_operator_supported(self):
        for rec in self:
            rec.chart_2_config_aggregate_operator_supported = rec.chart_2_config_aggregate_field_id.ttype in ['date', 'datetime']

    @api.depends('chart_1_config_aggregate2_field_id')
    def compute_chart_1_config_aggregate2_operator_supported(self):
        for rec in self:
            rec.chart_1_config_aggregate2_operator_supported = rec.chart_1_config_aggregate2_field_id.ttype in ['date', 'datetime']

    @api.depends('chart_2_config_aggregate2_field_id')
    def compute_chart_2_config_aggregate2_operator_supported(self):
        for rec in self:
            rec.chart_2_config_aggregate2_operator_supported = rec.chart_2_config_aggregate2_field_id.ttype in ['date', 'datetime']

    @api.onchange(
        'display_mode',
        'graph_type',
        'chart_1_config_aggregate_field_id', 'chart_1_config_aggregate_operator',
        'chart_2_config_aggregate_field_id', 'chart_2_config_aggregate_operator',
        'chart_1_config_show_empty_groups', 'chart_2_config_show_empty_groups'
    )
    def update_graph(self):
        for rec in self:
            rec.compute_dashboard_data()
            if hasattr(rec, 'compute_preview'):
                rec.compute_preview()


    def get_graph_color(self, color_index):
        colors = [ # Lospec.com/palette-list / NT1H / NatTorpedia
            '#acf693', '#46c657', '#158968', '#222f46', '#425d69', '#65908b', '#8fb9ac', '#bddfcc',
            '#abd1d2', '#8babbf', '#566a89', '#383a63', '#fff18d', '#edc660', '#de993c', '#c25e22', '#4b003b',
            '#8a0047', '#bc1334', '#e43636', '#ff9a70', '#9cd8fc', '#5e96dd', '#3953c0', '#19157f',
        ]

        color_index += 2

        if color_index < 0 or color_index >= len(colors):
            color_index = 0

        color = colors[color_index]
        color_index += 1

        return color, color_index

    def chart_get_data_query_1(self):
        if self.datasource == 'sql':
            return self.chart_get_data_query_sql_1()

        # add the context if it is set
        if self.query_1_config_context:
            try:
                additional_context = safe_eval(self.query_1_config_context)
                new_context = self.env.context.copy()
                new_context.update(additional_context)
                self.env.context = new_context
            except ValueError:
                pass

        return self.chart_get_data(
            self.get_query_1_domain(),
            self.query_1_config_model_id,
            self.get_group_by_tuple(self.query_1_config_measure_field_id, self.query_1_config_measure_operator, date_only_aggregate=False),
            [
                self.get_group_by_tuple(self.chart_1_config_aggregate_field_id, self.chart_1_config_aggregate_operator),
                self.get_group_by_tuple(self.chart_1_config_aggregate2_field_id, self.chart_1_config_aggregate2_operator),
            ],
            self.chart_1_config_show_empty_groups,
            self.action_id,
            title=self.chart_1_config_title,
            orderby="{} {}".format(self.chart_1_config_sort_field_id.name, "DESC" if self.chart_1_config_sort_descending else "ASC") if self.chart_1_config_sort_field_id else "",
            orderby_default_sort_label=self.chart_1_config_sort_default_by_label,
            limit=self.query_1_config_result_limit,
            sudo=self.query_1_sudo,
            query_name=self.chart_1_config_title,
            label_regx=self.label_1_regex,
        ), self.chart_1_config_color, self.chart_1_config_area, self.chart_1_config_title

    def chart_get_data_query_2(self):
        if self.datasource == 'sql':
            return self.chart_get_data_query_sql_2()

        # add the context if it is set
        if self.query_2_config_context:
            try:
                additional_context = safe_eval(self.query_2_config_context)
                new_context = self.env.context.copy()
                new_context.update(additional_context)
                self.env.context = new_context
            except ValueError:
                pass

        return self.chart_get_data(
            self.get_query_2_domain(),
            self.query_2_config_model_id,
            self.get_group_by_tuple(self.query_2_config_measure_field_id, self.query_2_config_measure_operator, date_only_aggregate=False),
            [
                self.get_group_by_tuple(self.chart_2_config_aggregate_field_id, self.chart_2_config_aggregate_operator),
                self.get_group_by_tuple(self.chart_2_config_aggregate2_field_id, self.chart_2_config_aggregate2_operator),
            ],
            self.chart_2_config_show_empty_groups,
            self.query_2_config_action_id,
            title=self.chart_2_config_title,
            orderby=False,  # TODO: Enable feature for query #2
            orderby_default_sort_label=self.chart_2_config_sort_default_by_label,
            limit=self.query_2_config_result_limit,
            sudo=self.query_2_sudo,
            query_name=self.chart_2_config_title,
            label_regx=self.label_2_regex,
        ), self.chart_2_config_color, self.chart_2_config_area, self.chart_2_config_title
