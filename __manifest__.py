# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Payment Scheduled Account',
    'version': '1.0',
    'category': 'Accounting',
    'description': """
Allows to create multiple account payments for the same transaction.
    """,
    'author': 'SYLEAM',
    'website': 'http://www.syleam.fr/',
    'depends': [
        'base',
        'account',
        'payment',
        'payment_account',
        'payment_scheduled',
    ],
    'data': [
    ],
    'installable': True,
    'license': 'AGPL-3',
}

