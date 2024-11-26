# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock module Actual Weight',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Track actual vs theoretical weights in warehouse operations',
    'author': 'Schumann Ye',
    'description': "",
    'depends': ['stock'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_line_views.xml',
        'views/stock_picking_views.xml',
    ],
}
