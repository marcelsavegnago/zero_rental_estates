# Copyright 2019 Zero for information systems(https://www.erpzero.com).

{
    'name': 'zero_rental_estate',
    'version': '11.0.1.0',
    'summary': """rental property management""",
    'description': """This module helps you to Manage rental property""",
    'category': 'real estate',
    'author': 'Zero Systems',
    'company': 'Zero for Information Systems',
    'website': "https://www.erpzero.com",
    'email': "sales@erpzero.com",
    'depends': ['base','mail','portal','resource','analytic',],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/city_districts_view.xml',
        'views/lessor_view.xml',
        'views/partner_view.xml',
        'views/payment_report.xml',
        'views/rental_view.xml',
        'views/estate_status_view.xml',
        'views/estate_view.xml',
        'views/potential_partner_view.xml',
    ],
    # only loaded in demonstration mode
    'images': ['static/description/logo.PNG'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
