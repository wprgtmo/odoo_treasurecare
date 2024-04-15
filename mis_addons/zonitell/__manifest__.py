# -*- coding: utf-8 -*-
{
    "name": "Zonitell",
    "summary": "Calls register of Zonitell App",
    "description": """
Calls register of Zonitell App used in TreaseureCare
    """,
    "author": "SmartDomino",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Calls",
    "version": "0.1",
    "application": True,
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/zonitell_call_contact_views.xml",
        "views/zonitell_call_views.xml",
        "views/zonitell_contact_views.xml",
        "views/menu_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
