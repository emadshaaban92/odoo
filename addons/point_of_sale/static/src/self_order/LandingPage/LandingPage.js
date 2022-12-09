/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { makeEnv, startServices } from "@web/env";
// import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
// import {  templates } from '@web/core/assets';
import { MainComponentsContainer } from "@web/core/main_components_container";
import { _t } from "@web/core/l10n/translation";

export class LandingPage extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
    // TODO: Add a method to get the table number from the response of the server
    getTableNumber() {
        return 12;
    }
}
LandingPage.template = 'LandingPage'
export default { LandingPage };