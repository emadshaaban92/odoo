/** @odoo-module */

import Chrome from "@point_of_sale/js/Chrome";
import { patch } from "@web/core/utils/patch";

patch(Chrome.prototype, "pos_france_certificate.Chrome", {
    async start() {
        await this._super();
        if (this.env.pos.is_french_country() && this.env.pos.pos_session.start_at) {
            const now = Date.now();
            const limitDate = new Date(this.env.pos.pos_session.start_at);
            limitDate.setDate(limitDate.getDate() + 1);
            if (limitDate.getTime() < now) {
                const info = await this.env.pos.getClosePosInfo();
                this.showPopup("ClosePosPopup", { info: info });
            }
        }
    },
});
