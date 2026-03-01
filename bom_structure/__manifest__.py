{
    'name': 'BoM Structure',
    'version': '19.0.1.0',
    'sequence':'2',
    'depends': ['mrp'],
    'summary':"Displays BoM Structure",
    'description': """
    This module Displays BoM Structure from BoM
    """,
    'author': 'Cybrosys',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/user_groups.xml',
        'views/mrp_bom.xml',

        ],
}