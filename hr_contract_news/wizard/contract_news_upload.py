# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2020 Jose Ernesto Mendez <jose.ernesto.mendez@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from openerp import models, fields, api, _
from openerp import exceptions # will be used in the code
import logging
_logger = logging.getLogger(__name__)
import base64
import csv
import cStringIO
#import datetime
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class ContractNewsUpload(models.TransientModel):
    _name = 'contract.news.upload.wizard'
    #_inherit = 'hr.payslip.run'

    data = fields.Binary('Cargar plantilla', required=False)
    template = fields.Binary("Descargar plantilla", readonly=True)
    template_name = fields.Char(u"Nombre de Reporte", size=40, readonly=True)
    delimeter = fields.Char('Delimitador', default=',',
                            help='Default delimeter is ","')
    contract_news_concepts_ids = fields.Many2many(comodel_name="hr_contract.news.concepts",
                                                  relation="", column1="", column2="", string="", )
    contract_type_id = fields.Many2one(comodel_name="hr.contract.type", string="Tipo de contrato", required=False, )

    @api.multi
    def do_generate_template(self):
        path = '/tmp/news_template.csv'
        f = open(path, 'w')
        header_str = ""
        header_str += "codigo_empleado,"
        header_str += "importe_descuento,"
        header_str += "aplicar_en,"
        header_str += "tipo_de_frecuencia,"
        header_str += "numero_de_veces,"
        header_str += "fecha_inicial,"

        f.write(header_str + '\n')

        f.close()

        f = open(path, 'rb')
        template = base64.b64encode(f.read())
        template_name = 'news_template.csv'
        self.write({'template': template, 'template_name': template_name})
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contract.news.upload.wizard',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def do_mass_update(self, args):
#	self.ensure_one()

        if not self.data:
            raise exceptions.Warning(_("Debe seleccionar un archivo!"))
        elif not self.contract_type_id:
            raise exceptions.Warning(_("Debe seleccionar un tipo de contrato!"))
        elif not self.contract_news_concepts_ids:
            raise exceptions.Warning(_("Debe seleccionar una novedad!"))

        if len(self.contract_news_concepts_ids) > 1:
            raise exceptions.Warning(_("Imposible cargar mas de una novedad por archivo!"))
        # Decode the file data
        data = base64.b64decode(self.data)
        file_input = cStringIO.StringIO(data)
        file_input.seek(0)
        reader_info = []
        if self.delimeter:
            delimeter = str(self.delimeter)
        else:
            delimeter = ','
        reader = csv.reader(file_input, delimiter=delimeter,
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        keys = reader_info[0]
        if not isinstance(keys, list) or ('codigo_empleado' not in keys or
                                          'importe_descuento' not in keys or
                                          'aplicar_en' not in keys or
                                          'tipo_de_frecuencia' not in keys):
            raise exceptions.Warning(
                _("No se han encontrado las claves 'codigo_empleado', "
                  "'importe_descuento', 'aplicar_en' y 'tipo_de_frecuencia' "
                  "en el documento! Por favor revise"))
        del reader_info[0]
        values = {}
        employee_obj = self.env['hr.employee']
        contract_obj = self.env['hr.contract']
        contract_id = 0
        contract_news_obj = self.env['hr.contract.news']
        type_id = self.contract_type_id.id

        for i in range(len(reader_info)):
            val = {}
            field = reader_info[i]
            values = dict(zip(keys, field))
            employee = employee_obj.search([('code', '=', values['codigo_empleado'])])
            current_date_time = datetime.now()
            current_date = current_date_time.strftime('%Y-%m-%d')
            if employee:
                #a contract is valid if it ends between the given dates
                #clause_1 = ['&',('employee_id', '=', employee_id)]
                #OR if it starts between the given dates
                #clause_2 = ['&',('type_id', '=', type_id)]
                #OR if it starts before the date_from and finish after the date_end (or never finish)
                clause_3 = ['|',('date_end', '=', False),('date_end','>=', current_date)]
                clause_final =  [('employee_id', '=', employee.id), ('type_id','=', type_id),] + clause_3

                contracts = contract_obj.search(clause_final)

                if contracts:
                    contracts_len = int(len(contracts.ids))
                    for contract in contracts:
                        contract_news = contract_news_obj.search([('contract_id', '=', contract.id),
                            ('hr_contract_news_concepts_id', '=', self.contract_news_concepts_ids.id)])
                        if contract_news and values['tipo_de_frecuencia'].lower() == 'fixed':
                            raise exceptions.Warning(_("Imposible aplicar un descuento tipo 'Fijo' mas de una "
                                                     "vez en el contrato %s de %s" % (contract.name,
                                                                                      contract.employee_id.name)))
                        else:
                            val['contract_id'] = contract.id
                            val['hr_contract_news_concepts_id'] = self.contract_news_concepts_ids.id
                            if contracts_len > 1:
                                val['amount'] = (float(values['importe_descuento']) / contracts_len)
                            else:
                                val['amount'] = values['importe_descuento']
                            val['apply_on'] = values['aplicar_en']
                            val['frecuency_type'] = values['tipo_de_frecuencia'].lower()
                            val['frecuency_number'] = int(values['numero_de_veces']) or 0
                            val['end_date'] = False
                            val['from_wizard'] = True
                            end_date = False

                            if values['tipo_de_frecuencia'].lower() == 'variable':
                                start_date = datetime.strptime(values['fecha_inicial'], '%d-%m-%Y').date() or False
                                frequency_number = (int(values['numero_de_veces'])-1) or 0
                                val['start_date'] = start_date
                                if values['aplicar_en'] == '1' or values['aplicar_en'] == '2':
                                    end_date = start_date + relativedelta(months=+frequency_number)
                                elif values['aplicar_en'] == '3':
                                    end_date = start_date + (relativedelta(months=+(frequency_number/2)) +
                                    relativedelta(days=+15))
                                val['end_date'] = end_date
                            contract_news_obj.create(val)

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contract.news.upload.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            }
