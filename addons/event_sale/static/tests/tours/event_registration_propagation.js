/** @odoo-module **/

import tour from 'web_tour.tour';

const initialSteps = [tour.stepUtils.showAppsMenuItem(), {
    trigger: '.o_app[data-menu-xmlid="sale.sale_menu_root"]',
}, {
    trigger: ".o_list_button_add",
    extra_trigger: ".o_sale_order",
}, {
    trigger: "a:contains('Add a product')",
}, {
    trigger: 'div[name="product_id"] input, div[name="product_template_id"] input',
    run: function (actions) {
        actions.text('Event Registration');
    },
}, {
    trigger: 'ul.ui-autocomplete a:contains("Event")',
    run: 'click',
}, {
    trigger: 'div[name="event_id"] input',
    run: 'click',
}, {
    trigger: 'ul.ui-autocomplete a:contains("Music")',
    run: 'click',
    in_modal: false,
}, {
    trigger: 'div[name="event_ticket_id"] input',
    run: 'click',
}, {
    trigger: 'ul.ui-autocomplete a:contains("VIP")',
    run: 'click',
    in_modal: false,
}, {
    trigger: '.o_event_sale_js_event_configurator_ok'
}, {
    trigger: 'div[name="product_uom_qty"]',
    run: 'click',
}, {
    trigger: 'div[name="product_uom_qty"] input',
    run: "text 2",
}, {
    content: "search the partner",
    trigger: 'div[name="partner_id"] input',
    run: 'text Azure',
}, {
    content: "select the partner",
    trigger: 'ul.ui-autocomplete > li > a:contains(Azure)',
}, {
    trigger: 'button[name="action_confirm"]',
    run: 'click',
}, {
    trigger: 'button[name="action_make_registration"]',
    run: 'click',
}];

tour.register('increase_registration_propagation_tour', {
    url: '/web',
    test: true,
}, [...initialSteps, {
    trigger: 'div[name="product_uom_qty"]',
    run: 'click',
}, {
    trigger: 'div[name="product_uom_qty"] input',
    run: "text 3",
}, {
    trigger: 'ul.nav a:contains("Order Lines")',
    run: 'click',
}, {
    trigger: 'button[name="action_make_registration"]',
    run: 'click',
}, ...tour.stepUtils.saveForm()]);

tour.register('decrease_registration_propagation_tour', {
    url: '/web',
    test: true,
}, [...initialSteps, {
    trigger: 'div[name="product_uom_qty"]',
    run: 'click',
}, {
    trigger: 'div[name="product_uom_qty"] input',
    run: "text 1",
}, {
    trigger: 'ul.nav a:contains("Order Lines")',
    run: 'click',
}, {
    trigger: 'td.o_list_record_remove button',
    extra_trigger: 'div[name="event_registration_ids"]',
    run: 'click',
}, {
    trigger: 'button[name="action_make_registration"]',
    run: 'click',
}, ...tour.stepUtils.saveForm()]);
