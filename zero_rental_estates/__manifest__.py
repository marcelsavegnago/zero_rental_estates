
# -*- coding: utf-8 -*-
{
    'name': "rental_estate_management",

    'summary': 'rental property management',

    'description': """rental property management""",

    'author': "zero systems",
    'website': "http:/www.erpzero.com",
    'category': 'real estate',
    'version': '11.0.0.1',
    'installable': True,
    'auto_install': False,
    'application': True,
     # any module necessary for this one to work correctly
    'depends': ['base','mail','portal','resource','analytic'],
    'images': ['static/description/logo.PNG'],
    # always loaded
    'data': ['security/security.xml','security/ir.model.access.csv','views/city_districts_view.xml','views/lessor_view.xml','views/partner_view.xml','views/payment_report.xml','views/potential_partner_view.xml','views/rental_view.xml','views/estate_status_view.xml','views/estate_view.xml',],
}
