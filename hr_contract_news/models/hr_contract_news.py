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
import openerp.addons.decimal_precision as dp
from openerp.exceptions import ValidationError
from itertools import permutations
from datetime import datetime
strptime = datetime.strptime
context_today = fields.Date.context_today
from_string = fields.Date.from_string

class HrContractNews(models.Model):
    _name = "hr.contract.news"
    _description = "News"
    contract_id = fields.Many2one(comodel_name="hr.contract", string="Contract", required=True, )
    hr_contract_news_concepts_id = fields.Many2one(comodel_name="hr_contract.news.concepts",
                                                   string="New", required=False, )
    amount = fields.Float(string="Amount",  required=False, digits_compute=dp.get_precision('Payroll'))
    frecuency_type = fields.Selection(string="Frequency type", selection=[('fixed', 'Fixed'),
                                                                              ('variable', 'Variable'), ],
                                      required=False, default='fixed', )
    apply_on = fields.Selection(string="Aplicar en", selection=[('1', 'Primera Quincena'),
                                                                ('2', 'Segunda Quincena'),
                                                                ('3', 'Primera y Segunda Quincena'), ],
                                required=False, )
    frecuency_number = fields.Integer(string="Number of times", required=False, )
    start_date = fields.Date(string="Initial date", required=False, )
    end_date = fields.Date(string="Final date", required=False, )
    from_wizard = fields.Boolean(string="From CSV?", readonly=True, )

    @api.one
    @api.constrains('hr_contract_news_concepts_id')
    def _check_overlapping_rates(self):
        """
        Checks if a rate has two lines that overlap in time.
        """
        for r1, r2 in permutations(self.hr_contract_news_concepts_id, 2):
            if (
                r1.end_date and
                r1.start_date <= r2.start_date <= r1.end_date
            ) or (
                not r1.end_date and
                r1.start_date <= r2.start_date
            ):
                raise ValidationError(
                    _('You cannot have overlapping rates'))


    def _get_amounts_now(self):
        today = context_today(self)
        self.amount = self.get_amount(today)

    @api.multi
    def get_amount(self, date):
        self.ensure_one()
        for line in self:
            if line.start_date <= date and (
                not line.end_date or date <= line.end_date
            ):
                return (
                    line.amount
                )
        return False

    @api.multi
    def compute_amounts(self, payslip):
        """
        Compute benefit lines
        """
        date_from = from_string(payslip.date_from)
        date_to = from_string(payslip.date_to)
        duration = (date_to - date_from).days + 1

        line_obj = self.env['hr.payslip.news.line']

        rate_lines = [
            line for line in self
            if (
                not line.end_date or payslip.date_from <= line.end_date
            ) and line.start_date <= payslip.date_to and (line.apply_on == payslip.payment_period
                                                          or line.apply_on == '3')
        ]

        for line in rate_lines:
            # base_ratio = self._get_line_base_ratio(line, payslip)
            #
            # duration_ratio = self._get_line_duration_ratio(
            #     line, date_from, date_to, duration)
            #
            # ratio = base_ratio * duration_ratio

            line_obj.create({
                'payslip_id': payslip.id,
                'hr_contract_news_concepts_id': line.hr_contract_news_concepts_id.id,
                'amount': line.amount,
                'source': 'contract',
                'reference': line.hr_contract_news_concepts_id.description,
            })
