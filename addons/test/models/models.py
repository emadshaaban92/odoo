# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

class test(models.Model):
    _name = 'test'
    _log_access = False

    name = fields.Char()
    line_ids = fields.One2many('test.line', 'test_id')

    int1 = fields.Integer('User', default=lambda x: 1)
    intx2 = fields.Integer('User', compute="_get_intx2", store=True)

    line_sum = fields.Integer('Sum Currency', compute='_line_sum', store=True)

    def pcache(self):
        print('------ Cache ----')
        for dd in self.env.cache._data.values():
            for field, ids in dd.items():
                for rid, value in ids.items():
                    print(field.model_name, rid,':', field.name,'=', value)
        print('')
        print('----- Todo -----')
        for field in self.env.all.todo:
            print(field, self.env.all.todo[field])
        print('')


    @api.depends('line_ids.intx2')
    def _line_sum(self):
        for record in self:
            total = 0
            for line in record.line_ids:
                total += line.intx2
            record.line_sum = total

    @api.depends('int1')
    def _get_intx2(self):
        for record in self:
            record.intx2 = record.int1 * 2

    def testme(self):
        t = time.time()
        main_id = self.create({
            'name': 'bla',
            'line_ids': [
                (0,0, {'name': 'abc'}),
                (0,0, {'name': 'def'}),
            ]
        })
        # main_id.int1 = 5
        # self.env['test.line'].create(
        #     {'name': 'ghi', 'test_id': main_id.id}
        # )
        # self.env['test.line'].search([('intx2', '=', 3)])
        return time.time()-t


class test_line(models.Model):
    _name = 'test.line'

    name = fields.Char()
    test_id = fields.Many2one('test')
    intx2   = fields.Integer(compute='_get_intx2', store=True)

    @api.depends('test_id.intx2')
    def _get_intx2(self):
        for record in self:
            record.intx2 = record.test_id.intx2


