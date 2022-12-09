/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { _t } from "@web/core/l10n/translation";
export class NavBar extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
//   static components = { LandingPageOutline };  
}
NavBar.template = 'NavBar'
export default { NavBar };
