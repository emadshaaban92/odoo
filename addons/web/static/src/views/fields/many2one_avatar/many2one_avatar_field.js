/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Many2OneField } from "../many2one/many2one_field";

import { Component } from "@odoo/owl";

export class Many2OneAvatarField extends Component {
    get relation() {
        return this.props.relation || this.props.record.fields[this.props.name].relation;
    }
    get many2oneProps() {
        return {...this.props};
    }
}

Many2OneAvatarField.template = "web.Many2OneAvatarField";
Many2OneAvatarField.components = {
    Many2OneField,
};
Many2OneAvatarField.props = {
    ...Many2OneField.props,
};

Many2OneAvatarField.supportedTypes = ["many2one"];

Many2OneAvatarField.extractProps = Many2OneField.extractProps;

registry.category("fields").add("many2one_avatar", Many2OneAvatarField);
