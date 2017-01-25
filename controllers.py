# -*- coding: utf-8 -*-
from openerp import http

# class Radius(http.Controller):
#     @http.route('/radius/radius/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/radius/radius/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('radius.listing', {
#             'root': '/radius/radius',
#             'objects': http.request.env['radius.radius'].search([]),
#         })

#     @http.route('/radius/radius/objects/<model("radius.radius"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('radius.object', {
#             'object': obj
#         })