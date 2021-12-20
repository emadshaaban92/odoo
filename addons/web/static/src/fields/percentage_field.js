/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { standardFieldProps } from "./standard_field_props";
import { PercentageEditor, PercentageViewer } from "./percentage";

const { Component } = owl;

export class PercentageField extends Component {
    /**
     * @param {Event} ev
     */
    onChange(ev) {
        let value = ev.target.value;
        if (this.props.record.fields[this.props.name].trim) {
            value = value.trim();
        }
        value = value / 100;
        this.props.update(value || false);
    }
}

Object.assign(PercentageField, {
    components: {
        PercentageEditor,
        PercentageViewer,
    },
    template: "web.PercentageField",
    props: {
        ...standardFieldProps,
    },

    displayName: _lt("Percentage"),
    supportedTypes: ["integer", "float"],
});

registry.category("fields").add("percentage", PercentageField);
