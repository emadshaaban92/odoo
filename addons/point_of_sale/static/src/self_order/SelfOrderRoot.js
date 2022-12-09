/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { makeEnv, startServices } from "@web/env";
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { _t } from "@web/core/l10n/translation";
import { LandingPage } from "./LandingPage/LandingPage.js";
class SelfOrderRoot extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
                console.log(this.vlad);
        });
    }
  static components = { LandingPage };  
}
SelfOrderRoot.template = "SelfOrderRoot";
export async function createPublicRoot() {
    await whenReady();
    const wowlEnv = makeEnv();
    await startServices(wowlEnv);
    const app = new App(SelfOrderRoot, {
        templates,
        env: wowlEnv,
        dev: wowlEnv.debug,
        translateFn: _t,
        translatableAttributes: ["data-tooltip"],
    });
    setLoadXmlDefaultApp(app);
    console.log("salut")
    return app.mount(document.body)
}
createPublicRoot();
export default { SelfOrderRoot, createPublicRoot };