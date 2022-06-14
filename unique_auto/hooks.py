# # -*- coding: utf-8 -*-

from odoo import api,SUPERUSER_ID

def post_init_hook_function(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    env['sale.order'].migrate_custom_data()
