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
        });
        this.state = useState({ currentScreen: 0, currentProduct: 0, cart: [] });
        const rpc = useService("rpc");
        this.menu = "";
        // this function makes a request to the server to get the menu
        onWillStart(async () => {
            this.productList = await rpc('/pos/self-order/get-menu');
        }); 
    }
    
    // productList = [
    //     {
    //         id: 0,
    //         name: "Coca-Cola",
    //         price: 2.5,
    //         description: "Coca-Cola is a carbonated soft drink manufactured by The Coca-Cola Company. Originally intended as a patent medicine, it was invented in the late 19th century by John Stith Pemberton and was bought out by businessman Asa Griggs Candler, whose marketing tactics led Coca-Cola to its dominance of the world soft-drink market throughout the 20th century.",
    //         image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",

    //     },
    // ];
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
    // TODO find function to remove product from cart
    removeProductFromCart = (id) =>{
        this.state.cart = this.state.cart.filter(item => item.id !== id);
 
        // this.state.cart.
    }
    getTotalCartQuantity = () =>{
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  cartItem.quantity;
        },0);
    }
    getTotalCartCost = () => {
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  this.productList[cartItem.id].list_price * cartItem.quantity;
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