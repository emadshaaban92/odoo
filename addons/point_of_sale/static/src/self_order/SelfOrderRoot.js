/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
import { makeEnv, startServices } from "@web/env";
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { _t } from "@web/core/l10n/translation";
import { LandingPageOutline } from "./LandingPage/LandingPageOutline/LandingPageOutline.js";
import { LandingPageStart } from "./LandingPage/LandingPageStart/LandingPageStart.js";
import { LandingPageEnd } from "./LandingPage/LandingPageEnd/LandingPageEnd.js";
import { NavBar } from "./NavBar/NavBar.js";
import { ProductMainView } from "./ProductMainView/ProductMainView.js";
class SelfOrderRoot extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
    //TODO: Add a method to get the table number from the response of the server
    tableNumber = 12;
    //TODO: Add a method to get the message from the response of the server
    message = "Your order is being processed";
    restaurantName = "Brasserie de Perwez";
    static components = { LandingPageOutline, LandingPageStart, LandingPageEnd, ProductMainView, NavBar };  
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