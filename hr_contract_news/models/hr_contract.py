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


class HrContract(models.Model):
    _inherit = "hr.contract"

    hr_contract_news_ids = fields.One2many(comodel_name="hr.contract.news", inverse_name="contract_id",
                                           string="News", required=False, )
    apply_specials_news = fields.Boolean(string="Apply special news?",  help="Check this field if this contract"
                                                                             " applies for incentive, travel refunds, etc.")