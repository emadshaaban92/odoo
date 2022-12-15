/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { makeEnv, startServices } from "@web/env";
// import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
// import {  templates } from '@web/core/assets';
import { MainComponentsContainer } from "@web/core/main_components_container";
import { _t } from "@web/core/l10n/translation";

export class LandingPageOutline extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
}
LandingPageOutline.template = 'LandingPageOutline'
export default { LandingPageOutline };
