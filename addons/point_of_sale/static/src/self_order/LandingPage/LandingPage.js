/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { makeEnv, startServices } from "@web/env";
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { MainComponentsContainer } from "@web/core/main_components_container";
import { _t } from "@web/core/l10n/translation";

export class LandingPage extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
    static template = xml`<h1>Hello Owl landing page</h1>`;
}
export default { LandingPage };