/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

export class GhostField extends Component {
    setup() {
        const info = this.props.record.fields[this.props.name];
        this.xmlId = info.xmlId;
    }
}

GhostField.template = xml`<span class="text-danger">missing field: <t t-esc="props.name"/></span>`;

registry.category("fields").add("ghost", GhostField);
