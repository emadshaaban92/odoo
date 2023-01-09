/** @odoo-module */

import ProductScreen from "@point_of_sale/js/Screens/ProductScreen/ProductScreen";
import { useBarcodeReader } from "@point_of_sale/js/custom_hooks";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, "pos_mercury.ProductScreen", {
    setup() {
        this._super();
        useBarcodeReader({
            credit: this.credit_error_action,
        });
    },
    credit_error_action() {
        this.showPopup("ErrorPopup", {
            body: this.env._t("Go to payment screen to use cards"),
        });
    },
});
