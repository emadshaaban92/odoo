# -*- coding: utf-8 -*-
from odoo.addons.account.tests.test_tax import TestTaxCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestTaxPython(TestTaxCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.python_tax = cls.env['account.tax'].create({
            'name': 'Python TAx',
            'amount_type': 'code',
            'amount': 0.0,
            'python_compute': 'result = ((price_unit * quantity) - ((price_unit * quantity) / 1.12)) * 0.5',
            'sequence': 1,
        })

    def test_tax_python_basic(self):
        res = self.python_tax.compute_all(130.0)
        self._check_compute_all_results(
            136.96, # 'total_included'
            130.0,  # 'total_excluded'
            [
                # base , amount    | seq | amount | incl | incl_base
                # --------------------------------------------------
                (130.0, 6.96),   # |  1  |    6%  |   t  |
                # --------------------------------------------------
            ],
            res
        )

    def test_tax_python_price_include(self):
        self.python_tax.price_include = True
        res = self.python_tax.compute_all(130.0)
        self._check_compute_all_results(
            130,    # 'total_included'
            123.04, # 'total_excluded'
            [
                # base , amount     | seq | amount | incl | incl_base
                # ---------------------------------------------------
                (123.04, 6.96),   # |  1  |    6%  |   t  |
                # ---------------------------------------------------
            ],
            res
        )

        res = (self.python_tax + self.python_tax).compute_all(130.0)
        self._check_compute_all_results(
            130,    # 'total_included'
            116.08, # 'total_excluded'
            [
                # base , amount     | seq | amount | incl | incl_base
                # ---------------------------------------------------
                (116.08, 6.96),   # |  1  |    6%  |   t  |
                (116.08, 6.96),   # |  1  |    6%  |   t  |
                # ---------------------------------------------------
            ],
            res
        )
