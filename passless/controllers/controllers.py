# -*- coding: utf-8 -*-
import logging
import json
import simplejson
from odoo import http
from ..models import PasslessSettings, map_receipt
import requests

_logger = logging.getLogger(__name__)

class Passless(http.Controller):

    @http.route('/passless/send', type='json', auth='public')
    def send(self, **kw):
        post_data = http.request.httprequest.get_data(as_text=True)
        post_json = simplejson.loads(post_data, use_decimal=True)
        _logger.info(post_data)
        receipt = post_json['params']['receipt']
        
        passlessReceipt = map_receipt(receipt)
        # settings = http.request.env['passless.settings']
        # atts = settings.get_values() # not working
        resp = requests.post('http://localhost:8080/send', data=passlessReceipt.to_json(), headers={'Content-type': 'application/json'})
        _logger.info(
            'Got response from nfc: status: %s, body: %s', 
            str(resp.status_code), 
            resp.text
        )
        return { "message": "Receipt received" }


    # @http.route('/passless/passless/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('passless.listing', {
    #         'root': '/passless/passless',
    #         'objects': http.request.env['passless.passless'].search([]),
    #     })

    # @http.route('/passless/passless/objects/<model("passless.passless"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('passless.object', {
    #         'object': obj
    #     })