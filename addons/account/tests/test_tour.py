# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.account.tests.common import AccountTestInvoicingHttpCommon
import odoo.tests


@odoo.tests.tagged('post_install_l10n', 'post_install', '-at_install')
class TestUi(AccountTestInvoicingHttpCommon):

    def test_01_account_tour(self):
        self.start_tour("/web", 'account_tour', login="admin")
