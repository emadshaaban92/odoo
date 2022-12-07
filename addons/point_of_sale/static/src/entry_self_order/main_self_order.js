odoo.define('point_of_sale.main_self_order', function(require) {
    'use strict';
const { Component, mount, xml } = owl;

// Owl Components
class Root extends Component {
  static template = xml`<div>Hello Owl</div>`;
}
mount(Root, document.body);
});