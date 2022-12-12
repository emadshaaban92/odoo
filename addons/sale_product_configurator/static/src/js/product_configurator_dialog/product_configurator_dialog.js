/** @odoo-module **/

import { Dialog } from '@web/core/dialog/dialog';
import { Product } from "../product/product";
import { formatMonetary } from "@web/views/fields/formatters";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useState } = owl;

export class ProductConfiguratorDialog extends Component {
    static components = { Dialog, Product};
    static template = 'sale_product_configurator.dialog';
    static props = {
        productTemplateId: { type: Number, optional: true },
        pricelistId: { type: Number, optional: true },
        currencyId: { type: Number, optional: true },
        mode: { type: String, optional: true, validate: (mode) => [
            // TODO Convert to Boolean
            "add", // show variant and/or optional products
            "edit", // Line already exists
        ].includes(mode) },
        close: { type: Function }, //TODO VCR REPLACE BY *
    };
    static defaultProps = {
        mode: "add",
    };

    setup() {
        this.title = this.env._t("Configure");
        this.rpc = useService("rpc");
        this.state = useState({
            quantity: 1,
        });

        onWillStart(async () => {
            this.data = await this.loadData();
        });
    }

    async loadData() {
        let { product, product_price } = await this.rpc('/sale_product_configurator/get_values', {
            product_template_id: this.props.productTemplateId,
            pricelist_id: this.props.pricelistId,
        });
        product_price = formatMonetary(product_price, {currencyId: this.props.currencyId});
        return { product, product_price }
    }

    _onConfirm() {
        // save
        this.props.close();
    }

    _onClose() {
        // remove the SO Line if not edit
        this.props.close();
    }
}
