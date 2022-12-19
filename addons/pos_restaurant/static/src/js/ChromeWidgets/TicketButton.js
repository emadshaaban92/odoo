/** @odoo-module */

import TicketButton from "@point_of_sale/js/ChromeWidgets/TicketButton";
import Registries from "@point_of_sale/js/Registries";

const PosResTicketButton = (TicketButton) =>
    class extends TicketButton {
        /**
         * If no table is set to pos, which means the current main screen
         * is floor screen, then the order count should be based on all the orders.
         */
        get count() {
            if (!this.env.pos || !this.env.pos.config) {
                return 0;
            }
            if (this.env.pos.config.iface_floorplan && this.env.pos.table) {
                return this.env.pos.getTableOrders(this.env.pos.table.id).length;
            } else {
                return super.count;
            }
        }

        _getLoadingOrderConditions() {
            return (super._getLoadingOrderConditions() || (
                this.env.pos.config.iface_floorplan &&
                !this.isTicketScreenShown &&
                !this.env.pos.table
            ));
        }
    };

Registries.Component.extend(TicketButton, PosResTicketButton);

export default TicketButton;
