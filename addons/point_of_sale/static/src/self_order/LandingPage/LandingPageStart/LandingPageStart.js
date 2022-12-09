/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { makeEnv, startServices } from "@web/env";
// import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
// import {  templates } from '@web/core/assets';
import { MainComponentsContainer } from "@web/core/main_components_container";
import { _t } from "@web/core/l10n/translation";
import { LandingPageOutline } from "../LandingPageOutline/LandingPageOutline.js";
export class LandingPageStart extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
  static components = { LandingPageOutline };  
}
LandingPageStart.template = 'LandingPageStart'
export default { LandingPageStart };
