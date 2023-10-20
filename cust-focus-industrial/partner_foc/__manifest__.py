{
    'name': "Partner - Focus Industrial",
    'summary': """Partner - Focus Industrial""",
    'description': """
    """,
    'author': "Inspired Software Pty Limited",
    'website': "http://www.inspiredsoftware.com.au",

    'category': 'Specific Industry Applications',
    'version': '14.0.1.1.0',

    'depends': [
        'base',
        'fieldservice', # oca-field-service
        'field_service_foc',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml'
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
