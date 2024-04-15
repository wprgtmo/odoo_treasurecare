# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ZonitellContacts(models.Model):    
    _name = 'res.partner'
    _inherit = 'res.partner'

    llamadas = fields.One2many(comodel_name='zonitell.calls', inverse_name='contact_caller')
