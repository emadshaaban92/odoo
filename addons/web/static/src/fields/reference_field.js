/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Many2OneField } from "./many2one_field";
import { standardFieldProps } from "./standard_field_props";

const { Component, useState, xml } = owl;

export class ReferenceField extends Component {
    setup() {
        this.state = useState({
            resModel: this.props.value && this.props.value.resModel,
        });
    }

    get m2oProps() {
        const p = {
            ...this.props,
            relation: this.relation,
            value: this.props.value && [this.props.value.resId, this.props.value.displayName],
            update: this.updateM2O.bind(this),
        };
        delete p.canSelectModel;
        return p;
    }

    get modelInfo() {
        return this.props.record.preloadedData[this.props.name];
    }

    get relation() {
        if (this.props.value && this.props.value.resModel) {
            return this.props.value.resModel;
        } else {
            return this.state.resModel;
        }
    }

    updateModel(value) {
        this.state.resModel = value;
        this.props.update(false);
    }

    updateM2O(value) {
        if (!this.state.resModel) {
            this.state.resModel = this.relation;
        }
        this.props.update(
            value && {
                resModel: this.state.resModel,
                resId: value[0],
                displayName: value[1],
            }
        );
    }
}

ReferenceField.template = xml/*xml*/ `
    <div class="o_row">
        <t t-if="!props.readonly and props.canSelectModel">
            <select class="o_input" t-on-change="(ev) => this.updateModel(ev.target.value || false)">
                <option />
                <t t-foreach="props.record.fields[props.name].selection" t-as="option" t-key="option[0]">
                    <option t-att-value="option[0]" t-att-selected="option[0] === relation" t-esc="option[1]" />
                </t>
            </select>
        </t>
        <t t-if="relation">
            <Many2OneField t-props="m2oProps" />
        </t>
    </div>
`;
ReferenceField.components = {
    Many2OneField,
};
ReferenceField.props = {
    ...standardFieldProps,
    canSelectModel: Boolean,
};

ReferenceField.extractProps = (fieldName, record, attrs) => {
    let charProps = {};
    if (record.fields[fieldName].type === "char") {
        const preloadedData = record.preloadedData[fieldName];
        charProps = {
            value: {
                resModel: preloadedData.model,
                resId: preloadedData.data.id,
                displayName: preloadedData.data.display_name,
            },
        };
    }

    return {
        canSelectModel: !attrs.options.model_field,
        ...charProps,
    };
};

registry.category("fields").add("reference", ReferenceField);
