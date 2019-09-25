# -*- coding: utf-8 -*-
{
    'name': "Extended Sequence",

    'summary': """
        Add an option to set date_range interval""",

    'description': """
        Add an option to set date_range interval
    """,

    'author': "Telexindo Bizmart",
    'website': "https://www.telexindo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Technical Settings',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/inherit_ir_sequence.xml',
    ],
}
