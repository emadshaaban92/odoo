/** @odoo-module */
// import { startWebClient } from "@web/start";
const { Component, mount, xml, onRendered } = owl;

// Owl Components
class Root extends Component {
    setup() {
        // console.log("Hello Owl");
        onRendered(() => {
                console.log('Rendered:', this.constructor.name);
        });
    }
  static template = xml`<div>Hello Owl</div>`;
}
setTimeout(() =>{
    mount(Root, document.body);
},1000);