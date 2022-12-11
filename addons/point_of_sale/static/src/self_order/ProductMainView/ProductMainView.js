/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { _t } from "@web/core/l10n/translation";
import { NavBar } from '../NavBar/NavBar.js';
export class ProductMainView extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
    product =       {
            name: "Coca-Cola",
            price: 2.5,
            description: "Coca-Cola is a carbonated soft drink manufactured by The Coca-Cola Company. Originally intended as a patent medicine, it was invented in the late 19th century by John Stith Pemberton and was bought out by businessman Asa Griggs Candler, whose marketing tactics led Coca-Cola to its dominance of the world soft-drink market throughout the 20th century.",
            image: "https://www.coca-cola.be/content/dam/journey/be/nl/private/brands/coca-cola/coca-cola.png",
        }
    static components = { NavBar };  
}
ProductMainView.template = 'ProductMainView'
export default { ProductMainView };
