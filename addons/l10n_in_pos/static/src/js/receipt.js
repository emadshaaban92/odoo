/** @odoo-module */

import { Orderline } from "@point_of_sale/js/models";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, "l10n_indian.Orderline", {
    export_for_printing() {
        var line = super.export_for_printing(...arguments);
        line.l10n_in_hsn_code = this.get_product().l10n_in_hsn_code;
        return line;
    },
});
