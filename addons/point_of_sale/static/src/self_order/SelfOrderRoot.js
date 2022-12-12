/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App, useState} = owl;
import { makeEnv, startServices } from "@web/env";
import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import { _t } from "@web/core/l10n/translation";
import { LandingPageOutline } from "./LandingPage/LandingPageOutline/LandingPageOutline.js";
import { LandingPageStart } from "./LandingPage/LandingPageStart/LandingPageStart.js";
import { LandingPageEnd } from "./LandingPage/LandingPageEnd/LandingPageEnd.js";
import { NavBar } from "./NavBar/NavBar.js";
import { ProductMainView } from "./ProductMainView/ProductMainView.js";
import { ProductList } from "./ProductList/ProductList.js";
class SelfOrderRoot extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
        this.state = useState({ currentScreen: 0, currentProduct: 0 });

    }

    productList = [
        {
            id: 0,
            name: "Coca-Cola",
            price: 2.5,
            description: "Coca-Cola is a carbonated soft drink manufactured by The Coca-Cola Company. Originally intended as a patent medicine, it was invented in the late 19th century by John Stith Pemberton and was bought out by businessman Asa Griggs Candler, whose marketing tactics led Coca-Cola to its dominance of the world soft-drink market throughout the 20th century.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",

        },
        {
            id: 1,
            name: "Fanta",
            price: 2.5,
            description: "Fanta is a brand of fruit-flavored carbonated soft drinks created by Coca-Cola in 1940. The original Fanta flavors were orange, lemon, and grape. In 1944, pineapple and lime were added to the line-up.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {
            id: 2,
            name: "Sprite",
            price: 2.5,
            description: "Sprite is a colorless, caffeine-free, lemon and lime-flavored soft drink created by The Coca-Cola Company. It was first developed in West Germany in 1959 as Fanta Klare Zitrone by the Coca-Cola owned Glas Cola company. Sprite was introduced in the United States in 1961 as a competitor to 7 Up. In 1963, the name was changed to Sprite, and the flavor was reformulated to be less sweet and more lemon-lime flavored. Sprite was introduced in the United Kingdom in 1964, and in Canada in 1965. Sprite is now available in more than 190 countries.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {   
            id: 3,
            name: "Coca-Cola Zero",
            price: 2.5,
            description: "Coca-Cola Zero Sugar is a sugar-free cola-flavored soft drink produced by The Coca-Cola Company. It is a variant of Coca-Cola, with an intense sweetener blend of aspartame, acesulfame potassium, and sucralose. Coca-Cola Zero Sugar was introduced in 2006 in the United States, and in 2007 in the United Kingdom.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
    ];
    //TODO: Add a method to get the table number from the response of the server
    tableNumber = 12;
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
    static components = { LandingPageOutline, LandingPageStart, LandingPageEnd, ProductMainView, NavBar, ProductList };  
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