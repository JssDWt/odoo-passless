# -*- coding: utf-8 -*-
import logging
import json
from odoo import http
from ..models import Settings, map_receipt
import requests

_logger = logging.getLogger(__name__)

class Passless(http.Controller):

    @http.route('/passless/send', type='json', auth='public')
    def send(self, **kw):
        receipt = kw.get('receipt')
        _logger.info("got receipt: " + json.dumps(receipt))
        
        passlessReceipt = map_receipt(receipt)
        settingsClass = Settings()
        settings = settingsClass.get_default_params()
        resp = requests.post(settings['nfc_url'], json=passlessReceipt)
        _logger.info(
            'Got response from nfc: status: %s, body: %s', 
            str(resp.status_code), 
            resp.text()
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