/** @odoo-module */

const { Component } = owl;
import { _t } from "@web/core/l10n/translation";
import { NavBar } from '../NavBar/NavBar.js';
export class ProductList extends Component {
    setup() {
    }
    static components = { NavBar };  
}
ProductList.template = 'ProductList'
export default { ProductList };

