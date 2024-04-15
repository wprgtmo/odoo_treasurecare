# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ZonitellContact(models.Model):    
    _name = 'res.partner'
    _inherit = 'res.partner'

    call_ids = fields.One2many(comodel_name='zonitell.call.contact', inverse_name="contact_id")
