# -*- coding: utf-8 -*-
{
    'name': "Accomplishment Report",

    'summary': """
        Unique International Export ltd co. accomplishment report
        module for Projects process. """,

    'description': """
    """,

    'author': "Elyon Solutions International Inc",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/inherit.xml',
        'reports/so_accomplishment_report.xml',
        'reports/report_binding.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
