/** @odoo-module */

import { registry } from "@web/core/registry";
import { useAutofocus, useService } from "@web/core/utils/hooks";
import { formatFloat } from "@web/views/fields/formatters";
import { FloatField } from '@web/views/fields/float/float_field';

const { useState } = owl;

export class SaleProductCatalogQuantity extends FloatField {
    setup() {
        super.setup();
        this.orm = useService("orm");

        const refName = 'numpadDecimal';
        useAutofocus({ refName });

        this.state = useState({
            readonly: this.props.readonly,
        });
    }

    get formattedValue() {
        return formatFloat(this.props.value, { noTrailingZeros: true });
    }

    setReadonly(readonly) {
        this.state.readonly = readonly;
    }

    removeQuantity() {
        if (this.props.value > 0) {
            this.props.update(this.props.value - 1);
        }
   }

    addQuantity() {
        this.props.update(this.props.value + 1);
    }

    // needed to trigger the onInput function of the useInputField in the FloatField Component
    onInput(_) {}
}

SaleProductCatalogQuantity.template = 'sale.SaleProductCatalogQuantity';
registry.category('fields').add('sale_product_catalog_quantity', SaleProductCatalogQuantity);
