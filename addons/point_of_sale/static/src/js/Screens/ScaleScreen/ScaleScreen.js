odoo.define('point_of_sale.ScaleScreen', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const TemporaryScreenMixin = require('@point_of_sale/js/Misc/TemporaryScreenMixin')[Symbol.for('default')];
    const { round_precision: round_pr } = require('web.utils');
    const Registries = require('point_of_sale.Registries');

    const { onMounted, onWillUnmount, useExternalListener, useState } = owl;

    class ScaleScreen extends TemporaryScreenMixin(PosComponent) {
        /**
         * @param {Object} props
         * @param {Object} props.product The product to weight.
         */
        setup() {
            super.setup();
            useExternalListener(document, 'keyup', this._onHotkeys);
            this.state = useState({ weight: 0 });
            onMounted(this.onMounted);
            onWillUnmount(this.onWillUnmount);
        }
        onMounted() {
            // start the scale reading
            this._readScale();
        }
        onWillUnmount() {
            // stop the scale reading
            this.env.proxy_queue.clear();
        }
        back() {
            this.closeWith(false);
        }
        confirm() {
            this.closeWith(true, {
                confirmed: true,
                payload: { weight: this.state.weight },
            });
        }
        _onHotkeys(event) {
            if (event.key === 'Escape') {
                this.back();
            } else if (event.key === 'Enter') {
                this.confirm();
            }
        }
        _readScale() {
            this.env.proxy_queue.schedule(this._setWeight.bind(this), {
                duration: 500,
                repeat: true,
            });
        }
        async _setWeight() {
            const reading = await this.env.proxy.scale_read();
            this.state.weight = reading.weight;
        }
        get _activePricelist() {
            const current_order = this.env.pos.get_order();
            let current_pricelist = this.env.pos.default_pricelist;
            if (current_order) {
                current_pricelist = current_order.pricelist;
            }
            return current_pricelist;
        }
        get productWeightString() {
            const defaultstr = (this.state.weight || 0).toFixed(3) + ' Kg';
            if (!this.props.product || !this.env.pos) {
                return defaultstr;
            }
            const unit_id = this.props.product.uom_id;
            if (!unit_id) {
                return defaultstr;
            }
            const unit = this.env.pos.units_by_id[unit_id[0]];
            const weight = round_pr(this.state.weight || 0, unit.rounding);
            let weightstr = weight.toFixed(Math.ceil(Math.log(1.0 / unit.rounding) / Math.log(10)));
            weightstr += ' ' + unit.name;
            return weightstr;
        }
        get computedPriceString() {
            return this.env.pos.format_currency(this.productPrice * this.state.weight);
        }
        get productPrice() {
            const product = this.props.product;
            return (product ? product.get_price(this._activePricelist, this.state.weight) : 0) || 0;
        }
        get productName() {
            return (
                (this.props.product ? this.props.product.display_name : undefined) ||
                'Unnamed Product'
            );
        }
        get productUom() {
            return this.props.product
                ? this.env.pos.units_by_id[this.props.product.uom_id[0]].name
                : '';
        }
    }
    ScaleScreen.template = 'ScaleScreen';

    Registries.Component.add(ScaleScreen);

    return ScaleScreen;
});
