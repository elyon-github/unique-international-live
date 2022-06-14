# -*- coding: utf-8 -*-
from odoo import http


class UniqueAuto(http.Controller):
    @http.route('/unique_auto/unique_auto', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/unique_auto/unique_auto/objects', auth='public')
    def list(self, **kw):
        return http.request.render('unique_auto.listing', {
            'root': '/unique_auto/unique_auto',
            'objects': http.request.env['unique_auto.unique_auto'].search([]),
        })

    @http.route('/unique_auto/unique_auto/objects/<model("unique_auto.unique_auto"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('unique_auto.object', {
            'object': obj
        })
