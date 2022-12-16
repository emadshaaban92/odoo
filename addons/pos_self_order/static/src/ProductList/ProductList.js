/** @odoo-module */

const { Component, onRendered } = owl;
import { _t } from "@web/core/l10n/translation";
import { NavBar } from '../NavBar/NavBar.js';
export class ProductList extends Component {
    setup() {
        onRendered(() => {
            console.log('Rendered:', this.constructor.name, this.props.restaurantName);
        });
    }
    
    static components = { NavBar };  
}
ProductList.template = 'ProductList'
export default { ProductList };

