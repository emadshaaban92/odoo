/** @odoo-module */

import { Gui } from "@point_of_sale/js/Gui";
import { PosGlobalState, Order, Orderline } from "@point_of_sale/js/models";
import core from "web.core";
import { patch } from "@web/core/utils/patch";

var _t = core._t;

patch(PosGlobalState.prototype, "l10n_france.PosGlobalState", {
    is_french_country() {
        var french_countries = ["FR", "MF", "MQ", "NC", "PF", "RE", "GF", "GP", "TF"];
        if (!this.company.country) {
            Gui.showPopup("ErrorPopup", {
                title: _t("Missing Country"),
                body: _.str.sprintf(
                    _t("The company %s doesn't have a country set."),
                    this.company.name
                ),
            });
            return false;
        }
        return _.contains(french_countries, this.company.country.code);
    },
    disallowLineQuantityChange() {
        const result = super.disallowLineQuantityChange(...arguments);
        return this.is_french_country() || result;
    },
});

patch(Order.prototype, "l10n_france.Order", {
    constructor() {
        super(...arguments);
        this.l10n_fr_hash = this.l10n_fr_hash || false;
        this.save_to_db();
    },
    export_for_printing() {
        var result = super.export_for_printing(...arguments);
        result.l10n_fr_hash = this.get_l10n_fr_hash();
        return result;
    },
    set_l10n_fr_hash(l10n_fr_hash) {
        this.l10n_fr_hash = l10n_fr_hash;
    },
    get_l10n_fr_hash() {
        return this.l10n_fr_hash;
    },
    wait_for_push_order() {
        var result = super.wait_for_push_order(...arguments);
        result = Boolean(result || this.pos.is_french_country());
        return result;
    },
    destroy(option) {
        // SUGGESTION: It's probably more appropriate to apply this restriction
        // in the TicketScreen.
        if (
            option &&
            option.reason == "abandon" &&
            this.pos.is_french_country() &&
            this.get_orderlines().length
        ) {
            Gui.showPopup("ErrorPopup", {
                title: _t("Fiscal Data Module error"),
                body: _t("Deleting of orders is not allowed."),
            });
        } else {
            super.destroy(...arguments);
        }
    },
});

patch(Orderline.prototype, "l10n_france.Orderline", {
    can_be_merged_with(orderline) {
        const order = this.pos.get_order();
        const orderlines = order.orderlines;
        const lastOrderline = order.orderlines.at(orderlines.length - 1);

        if (
            this.pos.is_french_country() &&
            (lastOrderline.product.id !== orderline.product.id || lastOrderline.quantity < 0)
        ) {
            return false;
        } else {
            return super.can_be_merged_with(...arguments);
        }
    },
});
