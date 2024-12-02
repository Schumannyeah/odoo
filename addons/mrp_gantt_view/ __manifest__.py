{
    'name': 'Manufacturing Orders Gantt View',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Gantt view for manufacturing orders with progress tracking',
    'description': '''
        This module adds a Gantt view to manufacturing orders, allowing you to:
        - Visualize manufacturing orders in a timeline
        - Track progress of each order
        - Filter and group orders by various criteria
        - View both list and Gantt representations
    ''',
    'author': 'Schumann Ye',
    'website': 'https://www.yourcompany.com',
    'depends': ['mrp', 'web_gantt'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_production_gantt_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}