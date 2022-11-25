# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class ProductConfiguratorController(http.Controller):
    @http.route(['/sale_product_configurator/get_values'], type='json', auth="user")
    def get_product_configurator_values(
        self,
        product_template_id,
        pricelist_id,
        quantity=1.0, # TODO no default
        product_template_attribute_value_ids=None, # expected list of ids or None
        *kw):
        product_template = request.env['product.template'].browse(int(product_template_id)).exists()
        pricelist = request.env['product.pricelist'].browse(int(pricelist_id)).exists()

        if product_template_attribute_value_ids:
            combination = request.env['product.template.attribute.value'].browse(product_template_attribute_value_ids)
        else:
            combination = product_template._get_first_possible_combination()

        product = product_template._get_variant_for_combination(combination)

        # Probably keep using get_combination_info
        if combination:
            no_variant_attributes_price_extra = [
                ptav.price_extra for ptav in combination.filtered(
                    lambda ptav:
                        ptav.price_extra and
                        ptav not in product.product_template_attribute_value_ids
                )
            ]
            if no_variant_attributes_price_extra:
                product = product.with_context(
                    no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
                )

        return dict(
            product=product.read(['id', 'description_sale', 'display_name'])[0], # ET SI TU N'EXISTAT PAS TODO Test with no variant
            product_price = pricelist._get_product_price(product or product_template, quantity)
        )

    @http.route(['/sale_product_configurator/configure'], type='json', auth="user", methods=['POST'])
    def configure(self, product_template_id, pricelist_id, **kw):
        add_qty = float(kw.get('add_qty', 1))
        product_template = request.env['product.template'].browse(int(product_template_id))
        pricelist = self._get_pricelist(pricelist_id)

        product_combination = False
        attribute_value_ids = set(kw.get('product_template_attribute_value_ids', []))
        attribute_value_ids |= set(kw.get('product_no_variant_attribute_value_ids', []))
        if attribute_value_ids:
            product_combination = request.env['product.template.attribute.value'].browse(attribute_value_ids)

        if pricelist:
            product_template = product_template.with_context(pricelist=pricelist.id, partner=request.env.user.partner_id)

        return request.env['ir.ui.view']._render_template(
            "sale_product_configurator.configure",
            {
                'product': product_template,
                'pricelist': pricelist,
                'add_qty': add_qty,
                'product_combination': product_combination
            },
        )

    @http.route(['/sale_product_configurator/show_advanced_configurator'], type='json', auth="user", methods=['POST'])
    def show_advanced_configurator(self, product_id, variant_values, pricelist_id, **kw):
        pricelist = self._get_pricelist(pricelist_id)
        return self._show_advanced_configurator(product_id, variant_values, pricelist, False, **kw)

    @http.route(['/sale_product_configurator/optional_product_items'], type='json', auth="user", methods=['POST'])
    def optional_product_items(self, product_id, pricelist_id, **kw):
        pricelist = self._get_pricelist(pricelist_id)
        return self._optional_product_items(product_id, pricelist, **kw)

    def _optional_product_items(self, product_id, pricelist, **kw):
        add_qty = float(kw.get('add_qty', 1))
        product = request.env['product.product'].browse(int(product_id))

        parent_combination = product.product_template_attribute_value_ids
        if product.env.context.get('no_variant_attribute_values'):
            # Add "no_variant" attribute values' exclusions
            # They are kept in the context since they are not linked to this product variant
            parent_combination |= product.env.context.get('no_variant_attribute_values')

        return request.env['ir.ui.view']._render_template("sale_product_configurator.optional_product_items", {
            'product': product,
            'parent_name': product.name,
            'parent_combination': parent_combination,
            'pricelist': pricelist,
            'add_qty': add_qty,
        })

    def _show_advanced_configurator(self, product_id, variant_values, pricelist, handle_stock, **kw):
        product = request.env['product.product'].browse(int(product_id))
        combination = request.env['product.template.attribute.value'].browse(variant_values)
        add_qty = float(kw.get('add_qty', 1))

        no_variant_attribute_values = combination.filtered(
            lambda product_template_attribute_value: product_template_attribute_value.attribute_id.create_variant == 'no_variant'
        )
        if no_variant_attribute_values:
            product = product.with_context(no_variant_attribute_values=no_variant_attribute_values)

        return request.env['ir.ui.view']._render_template("sale_product_configurator.optional_products_modal", {
            'product': product,
            'combination': combination,
            'add_qty': add_qty,
            'parent_name': product.name,
            'variant_values': variant_values,
            'pricelist': pricelist,
            'handle_stock': handle_stock,
            'already_configured': kw.get("already_configured", False),
            'mode': kw.get('mode', 'add'),
            'product_custom_attribute_values': kw.get('product_custom_attribute_values', None)
        })

    def _get_pricelist(self, pricelist_id, pricelist_fallback=False):
        return request.env['product.pricelist'].browse(int(pricelist_id or 0))
