/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

export class GhostField extends Component {
    setup() {
        this.info = this.props.record.fields[this.props.name];
    }

    get tooltipInfo() {
        return JSON.stringify({
            debug: !!odoo.debug,
            resModel: this.info.modelName,
            viewMode: this.info.viewMode,
            field: {
                name: this.info.name,
                help: `Field missing, check the console for more details`,
            },
        });
    }
}

GhostField.template = xml`
    <div t-att="{'data-tooltip-template': 'web.FieldTooltip', 'data-tooltip-info': tooltipInfo}">
        <span class="text-danger">
            missing field: <t t-esc="props.name"/>
        </span>
        <sup class="btn-link p-1" t-att="{'data-tooltip-template': 'web.FieldTooltip', 'data-tooltip-info': tooltipInfo}">?</sup>
    </div>`;

registry.category("fields").add("ghost", GhostField);
