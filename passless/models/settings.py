from odoo import models, fields, api

PARAMS = [
    ("nfc_url", "passless.nfc_url"),
]

class Settings(models.TransientModel):

    _name = 'passless.settings'
    _inherit = 'res.config.settings'

    nfc_url = fields.Char("nfc_url")

    @api.multi
    def set_params(self):
        self.ensure_one()
        
        value = getattr(self, 'nfc_url', 'http://raspberrypi.local/send')
        self.env['ir.config_parameter'].set_param('passless.nfc_url', value)

        # for field_name, key_name in PARAMS:
        #     value = getattr(self, field_name, '').strip()
        #     self.env['ir.config_parameter'].set_param(key_name, value)

    @api.multi
    def get_default_params(self):
        res = {}
        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '').strip()
        return res