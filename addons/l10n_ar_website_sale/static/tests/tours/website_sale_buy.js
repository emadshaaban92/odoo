odoo.define('l10n_ar_website_sale.shop_buy_product_tour', function (require) {
"use strict";

require('website_sale.tour');
let tour = require('web_tour.tour');

let shop_buy_product_tour = tour.tours.shop_buy_product;

if (shop_buy_product_tour.extra && (shop_buy_product_tour.extra.company_account_fiscal_country_code || "") === 'AR') {
    // Configure the AFIP Responsibility
    let go_checkout_step_idx = _.findIndex(shop_buy_product_tour.steps, step => step.trigger === 'a[href*="/shop/checkout"]');
    shop_buy_product_tour.steps.splice(go_checkout_step_idx + 1, 0, {
        content: "Fulfill shipping address form",
        trigger: 'select[name="country_id"]',
        run: function () {
            $('select[name="l10n_ar_afip_responsibility_type_id"] option').filter(function () {
                return $(this).html().trim() === "Consumidor Final";
            }).attr('selected', true);
            $('select[name="l10n_latam_identification_type_id"] option').filter(function () {
                return $(this).html().trim() === "Foreign ID";
            }).attr('selected', true);
            $('input[name="vat"]').val('12345678-9');
        },
    }, {
        content: "Click on Next button",
        trigger: '.oe_cart .btn:contains("Next")',
    }, {
        content: "Click on Confirm button",
        trigger: '.oe_cart .btn:contains("Confirm")',
    });
}
});
