/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App, useState, onWillStart} = owl;
import { makeEnv, startServices } from "@web/env";
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { _t } from "@web/core/l10n/translation";
import { LandingPageOutline } from "./LandingPage/LandingPageOutline/LandingPageOutline.js";
import { LandingPageStart } from "./LandingPage/LandingPageStart/LandingPageStart.js";
import { LandingPageEnd } from "./LandingPage/LandingPageEnd/LandingPageEnd.js";
import { NavBar } from "./NavBar/NavBar.js";
import { ProductMainView } from "./ProductMainView/ProductMainView.js";
import { ProductList } from "./ProductList/ProductList.js";
import { CartView } from "./CartView/CartView.js";
import { useService } from "@web/core/utils/hooks";


class SelfOrderRoot extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
                console.log("vlad", this.env)
        });
        this.state = useState({ currentScreen: 0, currentProduct: 0, cart: [] });
        const rpc = useService("rpc");
        // this function makes a request to the server to get the menu
        onWillStart(async () => {
            this.productList = await rpc('/pos/self-order/get-menu');
        }); 
    }
    jsonToString = (json) => {
        return JSON.stringify(json);
    }

    //TODO: Add a method to get the table number from the response of the server
    tableNumber = odoo.table_number;
    //TODO: Add a method to get the message from the response of the server
    message = "Your order is being processed";
    restaurantName = "Brasserie de Perwez";
    viewMenu = () => {
        this.state.currentScreen = 1;
    }
    viewProduct = (id) => {
        this.state.currentScreen = 2;
        this.state.currentProduct = id;
    }
    viewCart = () => {
        this.state.currentScreen = 3;
    }
    addToCart = (id, quantity) => {
        this.state.cart.push({id: id, quantity: quantity});
        this.state.currentScreen = 1;
    }
    removeProductFromCart = (id) =>{
        this.state.cart = this.state.cart.filter(item => item.id !== id);
    }
    getTotalCartQuantity = () =>{
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  cartItem.quantity;
        },0);
    }
    // this function returns the total price of the cart
    // 
    getTotalCartCost = () => {
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  this.productList.find(x => x.id === cartItem.id).list_price * cartItem.quantity;
        },0);
    }
    // TODO: Find the currency type of the posConfig
    // TODO: replace the euro sign string from the rest of the app with this variable
    currencyType = "€";
    static components = { LandingPageOutline, LandingPageStart, LandingPageEnd,
                         ProductMainView, NavBar, ProductList, CartView };  
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