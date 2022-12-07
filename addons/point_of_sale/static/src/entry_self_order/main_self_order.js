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
// startWebClient(Root);
// delay 3 seconds
setTimeout(() =>{
    mount(Root, document.body);
},5000);
// mount(Root, document.body);