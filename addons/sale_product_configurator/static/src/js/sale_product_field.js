/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { SaleOrderLineProductField } from '@sale/js/sale_product_field';
import { ProductConfiguratorDialog } from "./product_configurator_dialog/product_configurator_dialog";
import {
    selectOrCreateProduct,
    getSelectedVariantValues,
    getNoVariantAttributeValues,
} from "sale.VariantMixin";


patch(SaleOrderLineProductField.prototype, 'sale_product_configurator', {

    setup() {
        this._super(...arguments);

        this.dialog = useService("dialog");
        this.rpc = useService("rpc");
        this.ui = useService("ui");
    },

    async _onProductTemplateUpdate() {
        this._super(...arguments);
        const result = await this.orm.call(
            'product.template',
            'get_single_product_variant',
            [this.props.record.data.product_template_id[0]],
            {
                context: this.context,
            }
        );
        if(result && result.product_id) {
            if (this.props.record.data.product_id != result.product_id.id) {
                await this.props.record.update({
                    product_id: [result.product_id, result.product_name],
                });
                if (result.has_optional_products) {
                    this._openProductConfigurator('options');
                } else {
                    this._onProductUpdate();
                }
            }
        } else {
            if (!result.mode || result.mode === 'configurator') {
                this._openProductConfigurator('add');
            } else {
                // only triggered when sale_product_matrix is installed.
                this._openGridConfigurator(result.mode);
            }
        }
    },

    _editProductConfiguration() {
        this._super(...arguments);
        if (this.props.record.data.is_configurable_product) {
            this._openProductConfigurator('edit');
        }
    },

    get isConfigurableTemplate() {
        return this._super(...arguments) || this.props.record.data.is_configurable_product;
    },

    async _openProductConfigurator(mode) {
        const saleOrderRecord = this.props.record.model.root;

        this.dialog.add(ProductConfiguratorDialog, {
            productTemplateId: this.props.record.data.product_template_id[0],
            pricelistId: saleOrderRecord.data.pricelist_id[0],
            currencyId: saleOrderRecord.data.currency_id[0],
            // product_id
            // product_custom_attribute_value_data:
            // no_variant_attribute_values_data:
        });
        /* const $modal = $(
            await this.rpc(
                "/sale_product_configurator/configure",
                {
                    product_template_id: productTemplateId,
                    quantity: this.props.record.data.product_uom_qty || 1,
                    pricelist_id: pricelistId,
                    product_template_attribute_value_ids: this.props.record.data.product_template_attribute_value_ids.records.map(
                        record => record.data.id
                    ),
                    product_no_variant_attribute_value_ids: this.props.record.data.product_no_variant_attribute_value_ids.records.map(
                        record => record.data.id
                    ),
                    context: this.context,
                },
            )
        );
        const productSelector = `input[type="hidden"][name="product_id"], input[type="radio"][name="product_id"]:checked`;
        // TODO VFE drop this selectOrCreate and make it so that
        // get_single_product_variant returns first variant as well.
        // and use specified product on edition mode.
        const productId = await selectOrCreateProduct.call(
            this,
            $modal,
            parseInt($modal.find(productSelector).first().val(), 10),
            productTemplateId,
            false
        );
        $modal.find(productSelector).val(productId);
        const variantValues = getSelectedVariantValues($modal);
        const noVariantAttributeValues = getNoVariantAttributeValues($modal);
        const customAttributeValues = this.props.record.data.product_custom_attribute_value_ids.records.map(
            record => {
                // NOTE: this dumb formatting is necessary to avoid
                // modifying the shared code between frontend & backend for now.
                return {
                    custom_value: record.data.custom_value,
                    custom_product_template_attribute_value_id: {
                        res_id: record.data.custom_product_template_attribute_value_id[0],
                    },
                };
            }
        );
        this.rootProduct = {
            product_id: productId,
            product_template_id: productTemplateId,
            quantity: parseFloat($modal.find('input[name="add_qty"]').val() || 1),
            variant_values: variantValues,
            product_custom_attribute_values: customAttributeValues,
            no_variant_attribute_values: noVariantAttributeValues,
        }; */
        /* const optionalProductsModal = new OptionalProductsModal(null, {
            rootProduct: this.rootProduct,
            pricelistId: pricelistId,
            okButtonText: this.env._t("Confirm"),
            cancelButtonText: this.env._t("Back"),
            title: this.env._t("Configure"),
            context: this.context,
            mode: mode,
        }); */
    },

});
