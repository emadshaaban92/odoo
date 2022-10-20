/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { SaleOrderLineProductField } from '@sale/js/sale_product_field';
import { FloatField } from "@web/views/fields/float/float_field";
const { useEffect, useState } = owl;

patch(SaleOrderLineProductField.prototype, 'event_sale', {

    async _onProductUpdate() {
        this._super(...arguments);
        if (this.props.record.data.product_type === 'event') {
            this._openEventConfigurator();
        }
    },

    _editLineConfiguration() {
        this._super(...arguments);
        if (this.props.record.data.product_type === 'event') {
            this._openEventConfigurator();
        }
    },

    get isConfigurableLine() {
        return this._super(...arguments) || Boolean(this.props.record.data.event_ticket_id);
    },

    async _openEventConfigurator() {
        let actionContext = {
            'default_product_id': this.props.record.data.product_id[0],
        };
        if (this.props.record.data.event_id) {
            actionContext.default_event_id = this.props.record.data.event_id[0];
        }
        if (this.props.record.data.event_ticket_id) {
            actionContext.default_event_ticket_id = this.props.record.data.event_ticket_id[0];
        }
        this.action.doAction(
            'event_sale.event_configurator_action',
            {
                additionalContext: actionContext,
                onClose: async (closeInfo) => {
                    if (!closeInfo || closeInfo.special) {
                        // wizard popup closed or 'Cancel' button triggered
                        if (!this.props.record.data.event_ticket_id) {
                            // remove product if event configuration was cancelled.
                            this.props.record.update({
                                [this.props.name]: undefined,
                            });
                        }
                    } else {
                        const eventConfiguration = closeInfo.eventConfiguration;
                        this.props.record.update({
                            'event_id': eventConfiguration.event_id,
                            'event_ticket_id': eventConfiguration.event_ticket_id,
                        });
                    }
                }
            }
        );
    },
});

export class SaleOrderLineProductQuantityField extends FloatField {
    setup() {
        super.setup();
        this.action = useService("action");
        this.orm = useService("orm");
        this.uiService = useService("ui");
        this.state = useState({ value: this.props.value });
        useEffect(() => {
            if ((this.state.value !== this.props.value || this.props.record.isNew) && this.props.record.data.state === 'sale' && this.props.record.data.event_id) {
                this.state.value = this.props.value;
                this.update();
            }
        });
    }
    async update() {
        this.uiService.block();
        await this.props.record.model.root.save({ stayInEdition: true });
        const orderLineIds = this.props.record.model.root.data.order_line.resIds;
        const action = await this.env.model.orm.call("sale.order.line", "update_registrations_qty", [orderLineIds]);
        this.uiService.unblock();
        this.action.doAction(action);
        return true;
    }
}

registry.category("fields").add("sol_product_quantity", SaleOrderLineProductQuantityField);
