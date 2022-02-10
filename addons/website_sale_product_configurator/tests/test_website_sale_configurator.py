# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import tagged
from odoo.addons.sale_product_configurator.tests.common import TestProductConfiguratorCommon
from odoo.addons.base.tests.common import HttpCaseWithUserPortal


@tagged('post_install', '-at_install')
class TestWebsiteSaleProductConfigurator(TestProductConfiguratorCommon, HttpCaseWithUserPortal):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_product_custo_desk.write({
            'optional_product_ids': [(4, cls.product_product_conf_chair.id)],
            'website_published': True,
        })
        cls.product_product_conf_chair.website_published = True

        ptav_ids = cls.product_product_custo_desk.attribute_line_ids.product_template_value_ids
        ptav_ids.filtered(lambda ptav: ptav.name == 'Aluminium').price_extra = 50.4

    def test_01_product_configurator_variant_price(self):
        product = self.product_product_conf_chair.with_user(self.user_portal)
        ptav_ids = self.product_product_custo_desk.attribute_line_ids.product_template_value_ids
        parent_combination = ptav_ids.filtered(lambda ptav: ptav.name in ('Aluminium', 'White'))
        self.assertEqual(product._is_add_to_cart_possible(parent_combination), True)
        # This is a regression test. The product configurator menu is proposed
        # whenever a product has optional products. However, as the end user
        # already picked a variant, the variant configuration menu is omitted
        # in this case. However, we still want to make sure that the correct
        # variant attributes are taken into account when calculating the price.
        url = self.product_product_custo_desk.website_url
        # Ensure that no pricelist is available during the test.
        # This ensures that tours with triggers on the amounts will run properly.
        self.env['product.pricelist'].search([]).action_archive()
        self.start_tour(url, 'website_sale_product_configurator_optional_products_tour', login='portal')
