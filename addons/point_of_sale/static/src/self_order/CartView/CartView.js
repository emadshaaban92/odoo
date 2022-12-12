/** @odoo-module */

const { Component } = owl;
import { _t } from "@web/core/l10n/translation";
import { NavBar } from "../NavBar/NavBar.js";
export class CartView extends Component {
    setup() {
    }
    static components = { NavBar }; 
}
CartView.template = 'CartView'
export default { CartView };

