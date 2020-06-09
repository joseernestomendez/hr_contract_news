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


class HrContractNewsConcepts(models.Model):
    _name = 'hr_contract.news.concepts'
    _description = 'Contract News Concepts'

    active = fields.Boolean('Active', default=True)
    code = fields.Char(string='Code', size=8, required=False)
    name = fields.Char(string="Name", size=64, required=True)
    description = fields.Text(
        'Description',
        help="A brief explanation about this new."
    )

    contract_new_category_id = fields.Many2one(comodel_name="hr_contract.news.categories",
                                               string="Categoria Novedad", required=False, )
    salary_rule_ids = fields.Many2many('hr.salary.rule', 'salary_rule_contract_news_rel',
                                       'news_id', 'salary_rule_id', 'Salary Rules',)
    special_new= fields.Boolean(string="Novedad Especial",  )

