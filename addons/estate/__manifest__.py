# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Estate',
    'version': '1.0',
    'author': 'Schumann Ye',
    'description': "",
    'depends': ['base'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
