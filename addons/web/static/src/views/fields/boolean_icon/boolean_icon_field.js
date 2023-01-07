/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { standardFieldProps } from "../standard_field_props";

export class BooleanIconField extends Component {
    static defaultProps = {
        icon: "fa-check-square-o",
    };
    static extractProps = ({ attrs }) => {
        return {
            icon: attrs.options.icon,
        };
    };
    static template = "web.BooleanIconField";
    static props = {
        ...standardFieldProps,
        icon: { type: String },
    };
    static displayName = _lt("Boolean Icon");
    static supportedTypes = ["boolean"];
}

registry.category("fields").add("boolean_icon", BooleanIconField);
