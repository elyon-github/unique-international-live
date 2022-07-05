# -*- coding: utf-8 -*-
# from odoo import http


# class UniqueCustom(http.Controller):
#     @http.route('/unique_custom/unique_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unique_custom/unique_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('unique_custom.listing', {
#             'root': '/unique_custom/unique_custom',
#             'objects': http.request.env['unique_custom.unique_custom'].search([]),
#         })

#     @http.route('/unique_custom/unique_custom/objects/<model("unique_custom.unique_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unique_custom.object', {
#             'object': obj
#         })
