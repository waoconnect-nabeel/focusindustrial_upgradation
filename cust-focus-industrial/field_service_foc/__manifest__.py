{
    'name': "Focus - Field Service",
    'summary': """Focus - Field Service""",
    'description': """
    """,
    'author': "Inspired Software Pty Limited",
    'website': "http://www.inspiredsoftware.com.au",

    'category': 'Specific Industry Applications',
    'version': '13.0.1.1.0',

    'depends': [
        'base',
        'mail',
        'fieldservice',
        'fieldservice_stock',
        'fieldservice_sale_recurring',
        'sale',
        'sale_foc',
    ],
    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'reports/maintenance_report.xml',
        'views/fsm_template.xml',
        'views/fsm_service.xml',
        'views/fsm_equipment.xml',
        'views/fsm_person.xml',
        'views/fsm_order.xml',
        'views/fsm_recurring.xml',
        'views/fsm_recurring_template.xml',
        'views/res_partner.xml',
        'views/fsm_order_search_filters.xml',
        'views/fsm_order_button.xml',
        "views/fsm_calendar_popup_extend.xml",
        "views/fsm_location_extend.xml"
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
