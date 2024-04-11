# -*- coding: utf-8 -*-
# from odoo import http


# class Zonitell(http.Controller):
#     @http.route('/zonitell/zonitell', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/zonitell/zonitell/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('zonitell.listing', {
#             'root': '/zonitell/zonitell',
#             'objects': http.request.env['zonitell.zonitell'].search([]),
#         })

#     @http.route('/zonitell/zonitell/objects/<model("zonitell.zonitell"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('zonitell.object', {
#             'object': obj
#         })
