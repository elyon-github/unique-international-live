# -*- coding: utf-8 -*-
from odoo import http


class UniqueAr(http.Controller):
    @http.route('/unique_ar/unique_ar/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/unique_ar/unique_ar/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('unique_ar.listing', {
            'root': '/unique_ar/unique_ar',
            'objects': http.request.env['unique_ar.unique_ar'].search([]),
        })

    @http.route('/unique_ar/unique_ar/objects/<model("unique_ar.unique_ar"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('unique_ar.object', {
            'object': obj
        })
