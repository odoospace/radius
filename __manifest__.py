# -*- coding: utf-8 -*-
{
    'name': "radius",

    'summary': """
        FreeRadius module for WISPs""",

    'description': """
        FreeRadius module for WISPs
    """,

    'author': "Impulzia",
    'website': "http://www.impulzia.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Communication',
    'version': '11.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'account', 'contract'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/templates.xml',
        'cron.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
    #],
}
