from odoo import models, fields, _
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import ValidationError, UserError
from odoo import _
import logging


_logger= logging.getLogger(__name__)
class ZonitellCallImport(models.TransientModel):

    _name = "zonitell.call.import"
    _description = 'Zonitell Call Import'

    file = fields.Binary(string="File", required=True)


    def calls_import(self):
        try:
            wb = openpyxl.load_workbook(BytesIO(base64.b64decode(self.file)), read_only=True)
            ws = wb.active
          
            for record in ws.iter_rows(min_row=2,values_only=True):

                # Procesando Calls
                call = self.env['zonitell.call'].create({
                    'company_name': record[0],
                    'direction': record[1],
                    'status': record[2],
                    'extension': record[3],
                    'caller_id_name': record[4],
                    'caller_id_number': record[5],
                    'caller_destination': record[6],
                    'caller_destination_number':record[7],
                    'call_date': datetime.strptime(record[8], "%m/%d/%Y").date(),
                    'start_stamp':record[9],
                    'end_stamp':record[10],
                    'duration_seconds':record[11],
                    'missed_call': record[12],
                    'hangup_cause': record[13],
                    'notes': record[14],
                })

                #Procesando Contactos

                contact_name = str(record[4]).title()
                contact = self.env['res.partner'].search([('name', '=', contact_name)])
                if not contact:
                    contact=self.env['res.partner'].create({
                        # 'patient_id':patiend.id,
                        # 'contact_relation_id':relation.id,
                        'name': contact_name,
                        'phone': record[5]
                        })

                #_logger.debug(f'{call.id:10} ==> {contact.id:10}')

                #Procesando Relacion 

                # if call and contact:
                self.env['zonitell.call.contact'].create({
                        'call_id': call.id,
                        'contact_id': contact.id,
                        'direction' : record[1]
                    })

                # intake = self.env['hc.intake'].create({
                #     'start_date': datetime.strptime(record[25], "%m/%d/%Y").date(), 
                #     'end_date': datetime.strptime(record[26], "%m/%d/%Y").date(), 
                #     'start_care_date': datetime.strptime(record[24], "%m/%d/%Y").date(), 
                #     'note_diagnostic_primary': str(record[28]).title(),
                #     'note_diagnostic_secondary': str(record[29]).title(),
                #     'disciplines': str(record[30]).title(),
                #     'disciplines_frecuencies': str(record[31]).title(),
                #     'patient_id': patient.id,
                #     'physician_id': physician.id
                # })    
            




                        
                            


        except: 
            raise
            

