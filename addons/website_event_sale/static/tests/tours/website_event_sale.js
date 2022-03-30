odoo.define('website_event_sale.tour', function (require) {
'use strict';

var tour = require('web_tour.tour');

tour.register('event_buy_tickets', {
    test: true,
    url: '/event',
},
    [
        {
            content: "Go to the `Events` page",
            trigger: 'a[href*="/event"]:contains("Conference for Architects TEST"):first',
        },
        {
            content: "Select 1 unit of `Standard` ticket type",
            extra_trigger: '#wrap:not(:has(a[href*="/event"]:contains("Conference for Architects")))',
            trigger: 'select:eq(0)',
            run: 'text 1',
        },
        {
            content: "Check that the `VIP` ticket unit price is 1500",
            trigger: '.o_wevent_ticket_selector:eq(1) .o_wevent_registration_multi_select:contains("1500.00")',
            run: function () {}, // it's a check
        },
        {
            content: "Select 2 units of `VIP` ticket type",
            extra_trigger: 'select:eq(0):has(option:contains(1):propSelected)',
            trigger: 'select:eq(1)',
            run: 'text 2',
        },
        {
            content: "Check that the `VIP` ticket unit price has been updated to 1500 - 25% discount = 1125",
            trigger: '.o_wevent_ticket_selector:eq(1) .o_wevent_registration_multi_select:contains("1125.00")',
            run: function () {}, // it's a check
        },
        {
            content: "Check that the unit price has been updated to 1500 - 25% discount = 1125  and click on `Order Now` button",
            extra_trigger: 'select:eq(1):has(option:contains(2):propSelected)',
            trigger: '.btn-primary:contains("Register")',
        },
        {
            content: "Fill attendees details",
            trigger: 'form[id="attendee_registration"] .btn:contains("Continue")',
            run: function () {
                $("input[name='1-name']").val("Att1");
                $("input[name='1-phone']").val("111 111");
                $("input[name='1-email']").val("att1@example.com");
                $("input[name='2-name']").val("Att2");
                $("input[name='2-phone']").val("222 222");
                $("input[name='2-email']").val("att2@example.com");
                $("input[name='3-name']").val("Att3");
                $("input[name='3-phone']").val("333 333");
                $("input[name='3-email']").val("att3@example.com");
            },
        },
        {
            content: "Validate attendees details",
            extra_trigger: "input[name='1-name'], input[name='2-name'], input[name='3-name']",
            trigger: 'button:contains("Continue")',
        },
        {
            content: "Check that the cart contains exactly 3 triggers",
            trigger: 'a:has(.my_cart_quantity:containsExact(3)),.o_extra_menu_items .fa-plus',
            run: function () {}, // it's a check
        },
        {
            content: "go to cart",
            trigger: 'a:contains(Return to Cart)',
        },
        {
            content: "Now click on `Process Checkout`",
            extra_trigger: 'a:has(.my_cart_quantity):contains(3),#cart_products input.js_quantity[value="3"]',
            trigger: '.btn-primary:contains("Process Checkout")'
        },
        {
            content: "Check that the subtotal is 3,250.00 USD (1x 1000 + (2x 1500 at 25% discount) = 3250)", // this test will fail if the currency of the main company is not USD
            trigger: '#order_total_untaxed .oe_currency_value:contains("3,250.00")',
            run: function () {}, // it's a check
        },
        {
            content: "Check that the total is 3,575.00 USD (3250 + 10% tax = 3575)",
            trigger: '#order_total .oe_currency_value:contains("3,575.00")',
            run: function () {}, // it's a check
        },
        {
            content: "Select `Wire Transfer` payment method",
            trigger: '#payment_method label:contains("Wire Transfer")',
        },
        {
            content: "Pay",
            //Either there are multiple payment methods, and one is checked, either there is only one, and therefore there are no radio inputs
            // extra_trigger: '#payment_method input:checked,#payment_method:not(:has("input:radio:visible"))',
            trigger: 'button[name="o_payment_submit_button"]:visible:not(:disabled)',
        },
        {
            content: "Last step",
            trigger: '.oe_website_sale_tx_status:contains("Please use the following transfer details")',
            timeout: 30000,
        }
    ]
);

});
