/** @odoo-module */

const { Component, useState} = owl;
import { _t } from "@web/core/l10n/translation";
import { NavBar } from '../NavBar/NavBar.js';
import { IncrementCounter } from '../UtilComponents/IncrementCounter/IncrementCounter.js';
export class ProductMainView extends Component {
    setup() {
        this.state = useState({ quantity : 1  });
    }
    setQuantity = (quantity) => {
        if(this.state.quantity + quantity >= 0){
            this.state.quantity = quantity;
        }
    }
    static components = { NavBar, IncrementCounter };  
}
ProductMainView.template = 'ProductMainView'
export default { ProductMainView };
