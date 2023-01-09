/** @odoo-module */

import PosComponent from "@point_of_sale/js/PosComponent";
import { renderToString } from "@web/core/utils/render";

export class SaleDetailsButton extends PosComponent {
    static template = "SaleDetailsButton";
    static components = {};

    async onClick() {
        // IMPROVEMENT: Perhaps put this logic in a parent component
        // so that for unit testing, we can check if this simple
        // component correctly triggers an event.
        const saleDetails = await this.rpc({
            model: "report.point_of_sale.report_saledetails",
            method: "get_sale_details",
            args: [false, false, false, [this.env.pos.pos_session.id]],
        });
        const report = renderToString(
            "SaleDetailsReport",
            Object.assign({}, saleDetails, {
                date: new Date().toLocaleString(),
                pos: this.env.pos,
            })
        );
        const printResult = await this.env.proxy.printer.print_receipt(report);
        if (!printResult.successful) {
            await this.showPopup("ErrorPopup", {
                title: printResult.message.title,
                body: printResult.message.body,
            });
        }
    }
}
