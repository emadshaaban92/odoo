/** @odoo-module */

import PosComponent from "@point_of_sale/js/PosComponent";

export class SyncNotification extends PosComponent {
    static template = "SyncNotification";
    static components = {};

    onClick() {
        this.env.pos.push_orders(null, { show_error: true });
    }
}
