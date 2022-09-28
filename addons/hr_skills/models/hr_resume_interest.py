# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class HrEmployeeInterest(models.Model):
    _name = 'hr.resume.interest'
    _description = 'Employee Interest'
    _order = 'name'

    name = fields.Char('Name', required=True)
