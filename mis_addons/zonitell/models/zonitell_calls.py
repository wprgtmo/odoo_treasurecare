# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ZonitellCalls(models.Model):
    _name = "zonitell.calls"
    _description = "Zonitell calls"

    date = fields.Date()
    company_name = fields.Char(string="Company name")
    direction = fields.Char(string="Direction")
    status = fields.Char(string="Status")
    extension = fields.Char(string="Extension")
    caller_id_name = fields.Char(string="Caller Id name")
    caller_id_number = fields.Char(string="Caller Id number")
    caller_destination = fields.Char(string="Caller destination")
    caller_destination_number = fields.Char(
        string="Caller destination number"
    )
    call_date = fields.Char(string="Call date")
    start_stamp = fields.Char(string="Start stamp")
    end_stamp = fields.Char(string="End stamp")
    duration_seconds = fields.Char(string="Duration (seconds)")
    duration_minutes = fields.Integer(string="Duration (minutes)", compute="_get_duration_minutes")
    missed_call = fields.Char(string="Missed call")
    hangup = fields.Char(string="Hangup")
    cause = fields.Char(string="Cause")
    caller = fields.Many2one(comodel_name="zonitell.callers")
    contact_caller = fields.Many2one(comodel_name="res.partner")

    def _get_duration_minutes(self):
        for duration in self:
            if duration and (int(duration.duration_seconds) > 0):
                duration.duration_minutes = int(duration.duration_seconds) / 60
            else:
                duration.duration_minutes = 0
