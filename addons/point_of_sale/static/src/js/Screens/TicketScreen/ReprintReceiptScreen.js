/** @odoo-module */

import AbstractReceiptScreen from "@point_of_sale/js/Misc/AbstractReceiptScreen";

export class ReprintReceiptScreen extends AbstractReceiptScreen {
    static template = "ReprintReceiptScreen";
    setup() {
        super.setup();
        owl.onMounted(this.onMounted);
    }
    onMounted() {
        this.printReceipt();
    }
    confirm() {
        this.showScreen("TicketScreen", { reuseSavedUIState: true });
    }
    async printReceipt() {
        if (this.env.proxy.printer && this.env.pos.config.iface_print_skip_screen) {
            const result = await this._printReceipt();
            if (result) {
                this.showScreen("TicketScreen", { reuseSavedUIState: true });
            }
        }
    }
    async tryReprint() {
        await this._printReceipt();
    }
}
