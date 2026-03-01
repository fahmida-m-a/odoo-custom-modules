# -*- coding: utf-8 -*-
{
    'name': 'Account Recurring Payment',
    'version': '19.0.1.0',
    'sequence':'1',
    'depends': ['account'],
    'summary':"Account Recurring Payment",
    'category': 'Accounting',
    'description': """
    This module contains Account Recurring Payment.
    """,
    'author': 'Cybrosys',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'data':[
        'security/ir.model.access.csv',
        'wizard/recurring_entries_wizard.xml',
        'views/recurring_template.xml',
        ],

}