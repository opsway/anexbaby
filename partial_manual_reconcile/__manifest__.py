{
    "name": "Partial Reconcile",
    "summary": "Partial Manual Reconcile",
    "sequence": 15,
    "version": "15.0.1.0",
    'license': 'Other proprietary',
    'category': 'Accounting',
    "website": "",
    "author": "Maksym Koriahin",
    "maintainer": '',
    "application": True,
    'installable': True,
    'auto_install': False,
    "depends": [
        "account"
    ],
    "data": [
        'views/account_move_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            "/partial_manual_reconcile/static/src/js/reconciliation_model.js",
        ]
    },
}
