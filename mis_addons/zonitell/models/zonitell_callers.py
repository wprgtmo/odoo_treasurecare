# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ZonitellCallers(models.Model):
    _name = 'zonitell.callers'
    _description = 'Zonitell callers'

    first_name = fields.Char()
    last_name = fields.Char()
    full_name = fields.Char(compute="_get_full_name", store=True)
    phone_number = fields.Char()
    calls = fields.One2many(comodel_name='zonitell.calls', inverse_name='caller')

    @api.depends('first_name', 'last_name')
    def _get_full_name(self):
        for caller in self:
            cfn = caller.first_name if caller.first_name else ""
            cln = caller.last_name if caller.last_name else ""
            caller.full_name = cfn + " " + cln
