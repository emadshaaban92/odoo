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
            this.menu = await rpc('/pos/self-order/get-menu');
        }); 

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
        {   
            id: 4,
            name: "Burger",
            price: 5,
            description: "A hamburger, beefburger, burger or hamburg is a sandwich consisting of one or more cooked patties of ground meat, usually beef, placed inside a sliced bread roll or bun. The patty may be pan fried, barbecued, or flame broiled. Hamburgers are often served with cheese, lettuce, tomato, onion, pickles, bacon, or chiles.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg", 
        },
        {
            id: 5,
            name: "Fries",
            price: 3,
            description: "French fries, or simply fries, chips, finger chips, or French-fried potatoes, are batonnet or allumette-cut deep-fried potatoes. The potatoes are peeled and then sliced into uniform sticks about 12 to 25 mm (0.5 to 1 in) thick, depending on the variety and size of potato. They are then deep-fried in oil at 180 to 190 °C (356 to 374 °F) until golden brown.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {
            id: 6,
            name: "Chicken Nuggets",
            price: 4,
            description: "Chicken nuggets are chicken pieces made from chicken breast fillets or chicken thigh meat, formed into a small patty, breaded, and deep-fried. Chicken nuggets are a popular fast food item in the United States, Canada, the United Kingdom, Australia, New Zealand, and other countries.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {
            id: 7,
            name: "Chicken Burger",
            price: 5,
            description: "A hamburger, beefburger, burger or hamburg is a sandwich consisting of one or more cooked patties of ground meat, usually beef, placed inside a sliced bread roll or bun. The patty may be pan fried, barbecued, or flame broiled. Hamburgers are often served with cheese, lettuce, tomato, onion, pickles, bacon, or chiles.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg", 
        },
        {
            id: 8,
            name: "Chicken Fries",
            price: 3,
            description: "French fries, or simply fries, chips, finger chips, or French-fried potatoes, are batonnet or allumette-cut deep-fried potatoes. The potatoes are peeled and then sliced into uniform sticks about 12 to 25 mm (0.5 to 1 in) thick, depending on the variety and size of potato. They are then deep-fried in oil at 180 to 190 °C (356 to 374 °F) until golden brown.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {
            id: 9,
            name: "Chicken Nuggets",
            price: 4,
            description: "Chicken nuggets are chicken pieces made from chicken breast fillets or chicken thigh meat, formed into a small patty, breaded, and deep-fried. Chicken nuggets are a popular fast food item in the United States, Canada, the United Kingdom, Australia, New Zealand, and other countries.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {
            id: 10,
            name: "Burger",
            price: 5,
            description: "A hamburger, beefburger, burger or hamburg is a sandwich consisting of one or more cooked patties of ground meat, usually beef, placed inside a sliced bread roll or bun. The patty may be pan fried, barbecued, or flame broiled. Hamburgers are often served with cheese, lettuce, tomato, onion, pickles, bacon, or chiles.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg", 
        },
        {
            id: 11,
            name: "Fries",
            price: 3,
            description: "French fries, or simply fries, chips, finger chips, or French-fried potatoes, are batonnet or allumette-cut deep-fried potatoes. The potatoes are peeled and then sliced into uniform sticks about 12 to 25 mm (0.5 to 1 in) thick, depending on the variety and size of potato. They are then deep-fried in oil at 180 to 190 °C (356 to 374 °F) until golden brown.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        },
        {
            id: 12,
            name: "Chicken Nuggets",
            price: 4,
            description: "Chicken nuggets are chicken pieces made from chicken breast fillets or chicken thigh meat, formed into a small patty, breaded, and deep-fried. Chicken nuggets are a popular fast food item in the United States, Canada, the United Kingdom, Australia, New Zealand, and other countries.",
            image: "https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffoodsided.com%2Ffiles%2F2021%2F05%2FWendys-Daves-Triple.jpg",
        }
    ];


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
    getTotalCartQuantity = () =>{
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  cartItem.quantity;
        },0);
    }
    getTotalCartCost = () => {
        return this.state.cart.reduce((sum, cartItem) => {
            return sum +  this.productList[cartItem.id].price * cartItem.quantity;
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