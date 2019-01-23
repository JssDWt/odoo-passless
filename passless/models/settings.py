from odoo import models, fields, api
import logging

PARAMS = [
    ("nfc_url", "passless.nfc_url"),
]

_logger = logging.getLogger(__name__)

class PasslessSettings(models.TransientModel):

    _name = 'passless.settings'
    _inherit = 'res.config.settings'

    nfc_url = fields.Char("nfc_url")

    @api.multi
    def set_values(self):
        _logger.info("set_values called.")
        super(PasslessSettings, self).set_values()
        
        value = getattr(self, 'nfc_url', 'http://raspberrypi.local/send')
        _logger.info("current value: '" + str(value) + "'")
        self.env['ir.config_parameter'].sudo().set_param('passless.nfc_url', value)

        # for field_name, key_name in PARAMS:
        #     value = getattr(self, field_name, '').strip()
        #     self.env['ir.config_parameter'].set_param(key_name, value)

    def get_values(self):
        res = super(PasslessSettings, self).get_values()
        res.update(
            nfc_url=self.env['ir.config_parameter'].sudo().get_param('passless.nfc_url')
        )
        return res