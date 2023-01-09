/** @odoo-module */

import PosComponent from "@point_of_sale/js/PosComponent";

// Previously HeaderButtonWidget
// This is the close session button
class HeaderButton extends PosComponent {
    static template = "HeaderButton";
    static components = {};

    async onClick() {
        const info = await this.env.pos.getClosePosInfo();
        this.showPopup("ClosePosPopup", { info: info, keepBehind: true });
    }
}
