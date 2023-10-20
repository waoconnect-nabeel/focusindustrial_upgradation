{
    'name': 'Sale - Focus Industrial',
    'category': '',
    'website': 'http://www.inspiredsoftware.com.au',
    'summary': '',
    'version': '14.0.1.0.0',
    'description': """
        Focus Industrial - Sale Customisations
        """,
    'author': 'Inspired Software Pty Ltd',
    'depends': [
        'web',
        'account',
        'sale',
        'crm',
    ],
    'data': [
        'templates/layout_background.xml',
        'templates/invoice.xml',
        'templates/sale_order.xml',

        'views/account_payment_term.xml',
        'views/sale_order.xml',
        'views/crm_lead.xml',
        'views/crm_stage.xml',
        'views/sale_report.xml'
    ],
    'installable': True,
    'application': False,
}
