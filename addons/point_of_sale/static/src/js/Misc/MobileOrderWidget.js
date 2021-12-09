odoo.define('point_of_sale.MobileOrderWidget', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    const { onMounted } = owl;

    class MobileOrderWidget extends PosComponent {
        setup() {
            this.update();
            onMounted(() => {
                this.order.on('change', () => {
                    this.update();
                    this.render();
                });
                this.order.orderlines.on('change', () => {
                    this.update();
                    this.render();
                });
            });
        }
        get order() {
            return this.env.pos.get_order();
        }
        update() {
            const total = this.order ? this.order.get_total_with_tax() : 0;
            const tax = this.order ? total - this.order.get_total_without_tax() : 0;
            this.total = this.env.pos.format_currency(total);
            this.items_number = this.order ? this.order.orderlines.reduce((items_number,line) => items_number + line.quantity, 0) : 0;
        }
    }

    MobileOrderWidget.template = 'MobileOrderWidget';

    Registries.Component.add(MobileOrderWidget);

    return MobileOrderWidget;
});
