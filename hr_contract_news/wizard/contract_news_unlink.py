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
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


class ContractNewsUnlink(models.TransientModel):
    _name = 'contract.news.unlink.wizard'
    #_inherit = 'hr.payslip.run'

    contract_news_concepts_ids = fields.Many2many(comodel_name="hr_contract.news.concepts",
                                                  relation="", column1="", column2="", string="", )
    contract_type_id = fields.Many2one(comodel_name="hr.contract.type", string="Tipo de contrato", required=False, )

    @api.multi
    def do_mass_unlink(self, args):
        self.ensure_one()

        if not self.contract_type_id:
            raise exceptions.Warning(_("Debe seleccionar un tipo de contrato!"))
        elif not self.contract_news_concepts_ids:
            raise exceptions.Warning(_("Debe seleccionar al menos una novedad!"))


        values = {}
        employee_obj = self.env['hr.employee']
        contract_obj = self.env['hr.contract']
        contract_news_obj = self.env['hr.contract.news']
        type_id = self.contract_type_id.id

        #considerar hacer lista de todos los contratos y hacer el unlink global
        for item in self.contract_news_concepts_ids:
            contract_new = contract_news_obj.search([('contract_id.type_id', '=', type_id),
                                                     ('hr_contract_news_concepts_id', '=', item.id),
                                                     ('from_wizard', '=', True)])
            contract_new.unlink()

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'contract.news.upload.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            }
