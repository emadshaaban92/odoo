/** @odoo-module */

const { Component, mount, xml, onRendered, whenReady, App} = owl;
// import { setLoadXmlDefaultApp, loadJS, templates } from '@web/core/assets';
import {  templates } from '@web/core/assets';
import { MainComponentsContainer } from "@web/core/main_components_container";
import { _t } from "@web/core/l10n/translation";
import { NavBar } from '../NavBar/NavBar';
export class ProductView extends Component {
    setup() {
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
    productList = [
        {
            name: "Coca-Cola",
            price: 2.5,
            description: "Coca-Cola is a carbonated soft drink manufactured by The Coca-Cola Company. Originally intended as a patent medicine, it was invented in the late 19th century by John Stith Pemberton and was bought out by businessman Asa Griggs Candler, whose marketing tactics led Coca-Cola to its dominance of the world soft-drink market throughout the 20th century.",
            image: "https://www.coca-cola.be/content/dam/journey/be/nl/private/brands/coca-cola/coca-cola.png",
        },
        {
            name: "Fanta",
            price: 2.5,
            description: "Fanta is a brand of fruit-flavored carbonated soft drinks created by Coca-Cola in 1940. The original Fanta flavors were orange, lemon, and grape. In 1944, pineapple and lime were added to the line-up.",
            image: "https://www.coca-cola.be/content/dam/journey/be/nl/private/brands/fanta/fanta.png",
        },
        {
            name: "Sprite",
            price: 2.5,
            description: "Sprite is a colorless, caffeine-free, lemon and lime-flavored soft drink created by The Coca-Cola Company. It was first developed in West Germany in 1959 as Fanta Klare Zitrone by the Coca-Cola owned Glas Cola company. Sprite was introduced in the United States in 1961 as a competitor to 7 Up. In 1963, the name was changed to Sprite, and the flavor was reformulated to be less sweet and more lemon-lime flavored. Sprite was introduced in the United Kingdom in 1964, and in Canada in 1965. Sprite is now available in more than 190 countries.",
            image: "https://www.coca-cola.be/content/dam/journey/be/nl/private/brands/sprite/sprite.png",
        },
        {
            name: "Coca-Cola Zero",
            price: 2.5,
            description: "Coca-Cola Zero Sugar is a sugar-free cola-flavored soft drink produced by The Coca-Cola Company. It is a variant of Coca-Cola, with an intense sweetener blend of aspartame, acesulfame potassium, and sucralose. Coca-Cola Zero Sugar was introduced in 2006 in the United States, and in 2007 in the United Kingdom.",
            image: "https://www.coca-cola.be/content/dam/journey/be/nl/private/brands/coca-cola-zero-sugar/coca-cola-zero-sugar.png",
        },
    ];

  static components = { NavBar };  
}
ProductView.template = 'ProductView'
export default { ProductView };
