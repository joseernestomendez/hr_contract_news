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

{   'name': 'HR Employee Contract News',
    'version': '1.0.1',
    'images': ['static/description/main_screenshot.png'],
    'category': 'Generic Modules/Human Resources',
    'sequence': 20,
    'author': "Jose Ernesto Mendez <jose.ernesto.mendez@gmail.com>",
    'price': 180.99,
    'currency': 'USD',
    'summary': 'HR Employee Contract News',
    'description': """
Quick and Easy cash register process
===========================
    """,
    'depends': [
        'hr_payroll',
        'hr_payroll_account',
        'hr_salary_rule_reference',    ],
    'data': [
        'data/hr_contract.news.categories.csv',
        'data/hr_contract.news.concepts.csv',
        'data/hr.salary.rule.category.csv',
        'data/hr_salary_rule.xml',
        'views/hr_contract.xml',
        'views/hr_contract_news_categories.xml',
        'views/hr_contract_news_concepts.xml',
        'views/hr_payslip.xml',
        'views/hr_salary_rule.xml',
        'wizard/contract_news_upload.xml',
        'wizard/contract_news_unlink.xml',
    ],
    'installable': True,
    'application': False,
    'website': 'https://www.linkedin.com/in/jose-ernesto-mendez-diaz-29b7101a/',
}