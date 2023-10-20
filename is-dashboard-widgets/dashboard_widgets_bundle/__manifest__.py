# -*- coding: utf-8 -*-
{
    'name': 'Beautiful Powerful Dashboards (Bundle)',
    'category': 'Extra Tools',
    'website': 'https://www.odooinsights.com',
    'summary': "Beautiful powerful dashboards (bundle)",
    'version': '12.0.14.0',
    'description': """
Beautiful powerful dashboards. Create a dashboard for KPI&apos;s, alerts, teams, TV displays. 
Works with all Odoo module such as inventory, sales, purchasing, crm, and accounting. 
Use line graphs, pie charts, bar charts, stacked charts, radar charts, tables, KPI kanban cards.
Track goals and measure progress with estimated, forecast and variation tracking.
Easily create multiple dashboard screens and tag your dashboard items to keep your dashboard displays organised.
Watch our training videos for clear easy to follow instructions on creating your own simple and advanced dashboards.
Updated every two weeks. Please let us know any feature requests you have.
        """,
    'author': 'Inspired Software Pty Ltd',
    'live_test_url': 'https://www.inspiredsoftware.com.au/r/YTb',
    'depends': [
        'dashboard_widgets',
        'dashboard_widgets_account',
        'dashboard_widgets_purchase',
        'dashboard_widgets_sale',
        'dashboard_widgets_stock',
    ],
    'data': [
    ],
    'qweb': [
    ],
    'images': [
        'static/description/main_image.gif',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,

    'licence': 'OPL-1',
    'support': 'appsupport@inspiredsoftware.com.au',
    'price': '0',
    'currency': 'EUR',
}
