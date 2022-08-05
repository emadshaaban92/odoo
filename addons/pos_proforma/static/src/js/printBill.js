odoo.define('pos_pro_forma_order.PrintBillButton', function(require) {
    'use strict';

    const PrintBillButton = require('pos_restaurant.PrintBillButton');
    const Registries = require('point_of_sale.Registries');

    const PosProFormaPrintBillButton = PrintBillButton => class extends PrintBillButton {
        async onClick() {
            let order = this.env.pos.get_order();
            await this.env.pos.push_pro_forma_order(order);
            super.onClick();
        }
    };

    Registries.Component.extend(PrintBillButton, PosProFormaPrintBillButton);

    return PrintBillButton;
 });
