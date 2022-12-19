/** @odoo-module */

import { usePos } from "@point_of_sale/app/pos_store";
import PosComponent from "@point_of_sale/js/PosComponent";
import Registries from "@point_of_sale/js/Registries";

class TicketButton extends PosComponent {
    setup() {
        this.pos = usePos();
    }
    async onClick() {
        if (this.isTicketScreenShown) {
            this.env.posbus.trigger("ticket-button-clicked");
        } else {
            if (this._getLoadingOrderConditions()) {
                try {
                    this.env.pos.setLoadingOrderState(true);
                    await this.env.pos._syncAllOrdersFromServer();
                } finally {
                    this.env.pos.setLoadingOrderState(false);
                    this.showScreen("TicketScreen");
                }
            } else {
                this.showScreen("TicketScreen");
            }
        }
    }
    get isTicketScreenShown() {
        return this.pos.mainScreen.name === "TicketScreen";
    }
    get count() {
        if (this.env.pos) {
            return this.env.pos.get_order_list().length;
        } else {
            return 0;
        }
    }

    _getLoadingOrderConditions() {
        return this.env.pos.config.share_orders;
    }
}
TicketButton.template = "TicketButton";

Registries.Component.add(TicketButton);

export default TicketButton;
