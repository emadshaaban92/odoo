# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import re
import odoo.tests
from odoo.exceptions import ValidationError
from odoo.modules.module import get_manifest

_logger = logging.getLogger(__name__)

RE_ONLY = re.compile(r'QUnit\.(only|debug)\(')


def qunit_error_checker(message):
    # We don't want to stop qunit if a qunit is breaking.

    # '%s/%s test failed.' case: end message when all tests are finished
    if  'tests failed.' in message:
        return True

    # "QUnit test failed" case: one qunit failed. don't stop in this case
    if "QUnit test failed:" in message:
        return False

    return True  # in other cases, always stop (missing dependency, ...)


def generate_qunit_hash(module, testName='undefined'):
    name = module + '\x1C' + testName
    name_hash = 0

    for letter in name:
        name_hash = (name_hash << 5) - name_hash + ord(letter)
        name_hash |= 0

    hex_repr = hex(name_hash).lstrip('0x').zfill(8)
    return hex_repr[-8:]


@odoo.tests.tagged('post_install', '-at_install')
class QUnitSuiteCheck(odoo.tests.TransactionCase):

    def test_module_hash(self):
        self.assertEqual(generate_qunit_hash('web'), '61b27308')

    def test_test_assets_transpiled(self):
        files, remains = self.env['ir.qweb']._get_asset_content('web.qunit_suite_tests')
        self.assertFalse(remains)
        bundle = self.env['ir.qweb']._get_asset_bundle('web.qunit_suite_tests', files, env=self.env, css=False, js=True)
        not_transpiled = []
        for asset in bundle.javascripts:
            if not asset.is_transpiled:
                not_transpiled.append(asset.name)
        if not_transpiled:
            raise ValidationError('All test files should be transpiled:\n%s' % '\n'.join(not_transpiled))


@odoo.tests.tagged('post_install', '-at_install')
class QUnitSuite(odoo.tests.HttpCase, odoo.tests.CrossModule):

    @odoo.tests.no_retry
    def test_js(self):
        if 'web.qunit_suite_tests' in get_manifest(self.test_module)['assets']:
          #with self.profile(db='profiling', http=False):`
            module_hash = generate_qunit_hash(self.test_module)
            _logger.info('Starting qunit for module %s (%s)', self.test_module, module_hash)
            self.browser_js(f'/web/tests?moduleId={module_hash} ', "", "", login='admin', timeout=1800, error_checker=qunit_error_checker)
        else:
            _logger.info('No qunit test found for %s', self.test_module)

@odoo.tests.tagged('post_install', '-at_install')
class WebSuite(odoo.tests.HttpCase):
    def test_check_suite(self):
        # verify no js test is using `QUnit.only` as it forbid any other test to be executed
        self._check_only_call('web.qunit_suite_tests')
        self._check_only_call('web.qunit_mobile_suite_tests')

    def _check_only_call(self, suite):
        # As we currently aren't in a request context, we can't render `web.layout`.
        # redefinied it as a minimal proxy template.
        self.env.ref('web.layout').write({'arch_db': '<t t-name="web.layout"><head><meta charset="utf-8"/><t t-esc="head"/></head></t>'})

        assets = self.env['ir.qweb']._get_asset_content(suite)[0]
        if len(assets) == 0:
            self.fail("No assets found in the given test suite")

        for asset in assets:
            filename = asset['filename']
            if not filename or asset['atype'] != 'text/javascript':
                continue
            with open(filename, 'rb') as fp:
                if RE_ONLY.search(fp.read().decode('utf-8')):
                    self.fail("`QUnit.only()` or `QUnit.debug()` used in file %r" % asset['url'])


@odoo.tests.tagged('post_install', '-at_install')
class MobileWebSuite(odoo.tests.HttpCase):
    browser_size = '375x667'
    touch_enabled = True

    def test_mobile_js(self):
        # webclient mobile test suite
        self.browser_js('/web/tests/mobile?mod=web', "", "", login='admin', timeout=1800, error_checker=qunit_error_checker)
