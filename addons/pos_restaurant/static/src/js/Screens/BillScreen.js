/** @odoo-module */

import ReceiptScreen from "@point_of_sale/js/Screens/ReceiptScreen/ReceiptScreen";

export class BillScreen extends ReceiptScreen {
    static template = "BillScreen";
    confirm() {
        this.props.resolve({ confirmed: true, payload: null });
        this.trigger("close-temp-screen");
    }
    whenClosing() {
        this.confirm();
    }
    /**
     * @override
     */
    async printReceipt() {
        await super.printReceipt();
        this.currentOrder._printed = false;
    }
}
