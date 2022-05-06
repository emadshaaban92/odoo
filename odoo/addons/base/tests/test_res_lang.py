# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase

class test_res_lang(TransactionCase):

    def test_00_intersperse(self):
        from odoo.addons.base.models.res_lang import intersperse

        assert intersperse("", []) == ("", 0)
        assert intersperse("0", []) == ("0", 0)
        assert intersperse("012", []) == ("012", 0)
        assert intersperse("1", []) == ("1", 0)
        assert intersperse("12", []) == ("12", 0)
        assert intersperse("123", []) == ("123", 0)
        assert intersperse("1234", []) == ("1234", 0)
        assert intersperse("123456789", []) == ("123456789", 0)
        assert intersperse("&ab%#@1", []) == ("&ab%#@1", 0)

        assert intersperse("0", []) == ("0", 0)
        assert intersperse("0", [1]) == ("0", 0)
        assert intersperse("0", [2]) == ("0", 0)
        assert intersperse("0", [200]) == ("0", 0)

        assert intersperse("12345678", [1], '.') == ('1234567.8', 1)
        assert intersperse("12345678", [1], '.') == ('1234567.8', 1)
        assert intersperse("12345678", [2], '.') == ('123456.78', 1)
        assert intersperse("12345678", [2,1], '.') == ('12345.6.78', 2)
        assert intersperse("12345678", [2,0], '.') == ('12.34.56.78', 3)
        assert intersperse("12345678", [-1,2], '.') == ('12345678', 0)
        assert intersperse("12345678", [2,-1], '.') == ('123456.78', 1)
        assert intersperse("12345678", [2,0,1], '.') == ('12.34.56.78', 3)
        assert intersperse("12345678", [2,0,0], '.') == ('12.34.56.78', 3)
        assert intersperse("12345678", [2,0,-1], '.') == ('12.34.56.78', 3)
        assert intersperse("12345678", [3,3,3,3], '.') == ('12.345.678', 2)

        assert intersperse("abc1234567xy", [2], '.') == ('abc1234567.xy', 1)
        assert intersperse("abc1234567xy8", [2], '.') == ('abc1234567x.y8', 1) # ... w.r.t. here.
        assert intersperse("abc12", [3], '.') == ('abc12', 0)
        assert intersperse("abc12", [2], '.') == ('abc12', 0)
        assert intersperse("abc12", [1], '.') == ('abc1.2', 1)

    def test_available_lang(self):
        available_langs_code = self.env["res.lang"]._get_enabled_lang_code()
        installed_langs_code = [lang[0] for lang in self.env["res.lang"].get_installed()]
        self.assertTrue(len(available_langs_code) >= len(installed_langs_code))

        for lang in installed_langs_code:
            # Check that all installed languages are in the enabled languages
            self.assertIn(lang, available_langs_code)
            available_langs_code.remove(lang)

        default_langs = self.env["res.lang"].search([("code", "in", available_langs_code)])

        self.assertTrue(all(not lang.active for lang in default_langs))
