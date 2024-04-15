# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ZonitellCallContact(models.Model):    
    _name = 'zonitell.call.contact'
    _description = 'zonitell.call.contact'

    call_id = fields.Many2one(string='zonitell.call', comodel_name='zonitell.call')

    contact_id = fields.Many2one(string='zonitell.contact', comodel_name='zonitell.contact')
    
    direction = fields.Selection({'in':'In', 'out':'Out'})




