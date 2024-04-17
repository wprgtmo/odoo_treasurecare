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

    def create_contact(self, name, phone, is_company=False):
        name =  str(name).title() if name else "Sin nombre"
        phone = phone if phone else 0
        contact = self.env['res.partner'].search([('name', '=', name), ('phone', '=' , phone)])
        if not contact:
            contact= self.env['res.partner'].create({
                                            'name': name,
                                            'phone': phone,
                                            'is_company': is_company,
                                            })
        return contact

    def create_extension_contact(self, name, ext, parent):
        name = str(name).title() if name else "Sin extension"
        ext = ext if ext else 0
        parent = parent if parent else 0
        extension = self.env['res.partner'].search([('name', '=', name), ('phone', '=', ext), ('parent_id', '=', parent)])
        if not extension:   
            extension= self.env['res.partner'].create({
                                            'name': name,
                                            'phone': ext,
                                            'is_company': False,
                                            'parent_id':  parent,
                                            'commercial_partner_id': parent,
                                            })
        return extension


    def update_extension_contact(self, name, ext, parent):
        extension = self.env['res.partner'].search([('phone', '=', ext), ('parent_id', '=', parent)])
        extension.name = name

    def create_duracere_contacts(self): 
        duracare= self.create_contact('Duracare Home Health Services', '7137820551', True)
        # self.create_extension_contact('SARAY','101', duracare.id)
        # self.create_extension_contact('THAIS','102', duracare.id)
        # self.create_extension_contact('JEANETTE','103', duracare.id)
        # self.create_extension_contact(duracare.name,duracare.id, duracare.id)
        return duracare

    def create_call(self, record)->any:
        return self.env['zonitell.call'].create({
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

    def create_relation(self, call, contact, direction):
        return self.env['zonitell.call.contact'].create({
            'call_id': call,
            'contact_id': contact,
            'direction' : direction
        })

    def clean(self):
        self.env['zonitell.call'].search([]).unlink()
        self.env['res.partner'].search([('phone', '!=', '+1 813-505-3406')]).unlink()
        self.env['zonitell.call.contact'].search([]).unlink()


    def calls_import(self):
        try:
            self.clean()
            duracare = self.create_duracere_contacts()
            wb = openpyxl.load_workbook(BytesIO(base64.b64decode(self.file)), read_only=True)
            ws = wb.active
          
            for record in ws.iter_rows(min_row=2,values_only=True):

                if record[1]=='outbound': # The calls is outbound
                    # Procesando Calls
                    call= self.create_call(record)

                    #Procesando Contactos
                    extension = self.create_extension_contact(record[3], record[3], duracare.id)
                    contact= self.create_contact(record[6] , record[7]) 

                    #Procesando Relacion 
                    self.create_relation(call.id, extension.id, 'out')
                    self.create_relation(call.id, contact.id, 'in')

                if record[1]=='inbound': # The calls is inbound
                    # Procesando Calls
                    call= self.create_call(record)

                    #Procesando Contactos
                    extension = self.create_extension_contact(record[3], record[3], duracare.id)
                    contact= self.create_contact(record[4] , record[5]) 

                    #Procesando Relacion 
                    self.create_relation(call.id, extension.id, 'in')
                    self.create_relation(call.id, contact.id, 'out')    


                if record[1]=='local': # The calls is inbound
                    # Procesando Calls
                    call= self.create_call(record)

                    #Procesando Contactos
                    dest = self.create_extension_contact(record[3], record[3], duracare.id)
                    origen= self.create_extension_contact(record[4] , record[5], duracare.id) 

                    #Procesando Relacion 
                    self.create_relation(call.id, dest.id, 'in')
                    self.create_relation(call.id, origen.id, 'out')                                         

            self.update_extension_contact('SARAY','101', duracare.id)
            self.update_extension_contact('THAIS','102', duracare.id)
            self.update_extension_contact('JEANETTE','103', duracare.id)
        except: 
            raise
            

