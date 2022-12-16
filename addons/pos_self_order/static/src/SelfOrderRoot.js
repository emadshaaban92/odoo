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

// This is the Root Component of the SelfOrder App
// Most of the business logic is done here
// The app has the folowing screens:
// 0. LandingPageStart  -- the first screen that the user sees -- it has a button that redirects to the menu
// 1. ProductList -- the screen that shows the list of products ( the menu )
// 2. ProductMainView  -- the screen that shows the details of a product ( the product page )
// 3. CartView  -- the screen that shows the cart
// 4. LandingPageEnd -- the screen that shows the order confirmation  --  it has a button that redirects to the menu


class SelfOrderRoot extends Component {
    setup() {
        /*
        In the state we store the following information:
            currentScreen: int -- the id of the current screen
            -------------------
            currentProduct: int -- the id of the product that is currently displayed in the ProductMainView
            -------------------
            cart: [] -- the cart is an array of objects that have the following structure:
            {
                id: 0, -- the id of the product
                quantity: 0 -- the quantity of the product
            }
        */
        this.state = useState({ currentScreen: 0, currentProduct: 0, cart: [] });
        this.rpc = useService("rpc");

        // this function makes a request to the server to get the menu
        onWillStart(async () => {
            this.productList = await this.rpc('/pos-self-order/get-menu');
        }); 

    }
    jsonToString = (json) => {
        return JSON.stringify(json);
    }
    // FIXME we have to use the function that correctly formats the price (with the currency symbol and the correct number of decimals)
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
    getTotalCartCost = () => {
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  this.productList.find(x => x.id === cartItem.id).list_price * cartItem.quantity;
        },0);
    }
    sendOrder = async () => {
        this.response_after_order = await this.rpc('/pos-self-order/send-order', { cart: this.state.cart });
        // this.state.currentScreen = 4;
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
    return app.mount(document.body)
}
createPublicRoot();
export default { SelfOrderRoot, createPublicRoot };