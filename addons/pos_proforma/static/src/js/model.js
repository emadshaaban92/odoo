odoo.define('pos_pro_forma_order.models', function (require) {
    "use strict";

    const Registries = require('point_of_sale.Registries');
    const { PosGlobalState, Order } = require('point_of_sale.models');

    const PosProFormaPosGlobalState = (PosGlobalState) => class PosProFormaPosGlobalState extends PosGlobalState {
        async push_pro_forma_order(order) {
            order.receipt_type = "PS";
            await this.env.pos.push_single_order(order);
            order.receipt_type = false;
        }
        async push_single_order(order, opts) {
            return await super.push_orders.apply(this, arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, PosProFormaPosGlobalState);

    const PosProFormaOrder = (Order) => class PosProFormaOrder extends Order {
        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.receipt_type = this.receipt_type;
            return json;
        }
    }
    Registries.Model.extend(Order, PosProFormaOrder);
});
