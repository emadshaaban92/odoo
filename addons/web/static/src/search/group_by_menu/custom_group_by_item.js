/** @odoo-module **/

import { Dropdown } from "@web/core/dropdown/dropdown";

import { Component, useState } from "@odoo/owl";

export class CustomGroupByItem extends Component {
    async setup() {
        this.state = useState({});
        if (this.props.fields.length) {
            this.state.fieldName = this.props.fields[0].name;
        }

        this.fields = await this._initializeFields();
    }

    /**
     * Initialize the fields to display in the select menu.
     *
     * Remove the properties fields and replace them
     * by their corresponding properties.
     */
    async _initializeFields() {
        if (!this.env || !this.env.searchModel
            || !this.env.searchModel.fillSearchViewItemsProperty) {
            return this.props.fields;
        }

        await this.env.searchModel.fillSearchViewItemsProperty();

        const allFields = Object.values(this.env.searchModel.searchViewFields);

        return [
            ...this.props.fields.filter(field => field.type !== 'properties'),
            ...allFields.filter(field => field.isProperty),
        ];
    }
}

CustomGroupByItem.template = "web.CustomGroupByItem";
CustomGroupByItem.components = { Dropdown };
CustomGroupByItem.props = {
    fields: Array,
    onAddCustomGroup: Function,
};
