odoo.define('l10n_it_edi.account_tour', function (require) {
"use strict";

require('account.tour');
var core = require('web.core');
let tour = require('web_tour.tour');

var _t = core._t;

let account_tour = tour.tours.account_tour;

if (account_tour.extra && (account_tour.extra.company_account_fiscal_country_code || "") === 'IT') {
    // Configure the partner address and vat
    let partner_step_idx = _.findIndex(account_tour.steps, step => step.trigger === 'div[name=partner_id] input');
    account_tour.steps.splice(partner_step_idx + 2, 0, {
        trigger: "input[name=street]",
        position: "right",
        content: "Set a Street",
        run: "text Test Street 123",
    }, {
        trigger: "input[name=city]",
        position: "right",
        content: "Set a City",
        run: "text Rome",
    }, {
        trigger: "input[name=zip]",
        position: "right",
        content: "Set a Zip Code",
        run: "text 39020",
    }, {
        trigger: "div[name=country_id] input",
        position: "right",
        content: "Set a country",
        run: "text Italy",
    }, {
        trigger: ".ui-menu-item > a:contains('Italy').ui-state-active",
        auto: true,
        in_modal: false,
    }, {
        trigger: "div[name=vat] input",
        position: "bottom",
        content: "Set a VAT",
        run: "text IT07643520567",
    });
}
});
