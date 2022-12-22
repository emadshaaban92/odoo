/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";

export class ViewScaleButton extends Component {
    static components = {
        Dropdown,
        DropdownItem,
    };
    static template = "web.ViewScaleButton";
    static props = {
        scales: { type: Object },
        currentScale: { type: String },
        setScale: { type: Function },
    };
}
