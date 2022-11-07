odoo.define('l10n_cl.account_tour', function (require) {
"use strict";

require('account.tour');
let tour = require('web_tour.tour');

let account_tour = tour.tours.account_tour;
if (account_tour.extra && (account_tour.extra.company_account_fiscal_country_code || "") === 'CL') {
    let partner_step_idx = _.findIndex(account_tour.steps, step => step.trigger === 'div[name=partner_id] input');
    // Configure the partner country
    account_tour.steps.splice(partner_step_idx + 2, 0, {
        trigger: "div[name=country_id] input",
        position: "bottom",
        content: "Select a country for the partner",
        run: "text Chile",
    }, {
        trigger: ".ui-menu-item > a:contains('Chile').ui-state-active",
        auto: true,
        in_modal: false,
    },
    // Configure the Identification Type and Number
    {
        trigger: "div[name=l10n_latam_identification_type_id] input",
        position: "bottom",
        content: "Set the Identification Type",
        run: "text Foreign ID",
    }, {
        trigger: ".ui-menu-item > a:contains('Foreign ID').ui-state-active",
        auto: true,
        in_modal: false,
    }, {
        trigger: "input[name=vat]",
        position: "bottom",
        content: "Set the Identification Number",
        run: "text 12345678-9",
    },
    // Configure the Taxpayer Type
    {
        trigger: "select[name=l10n_cl_sii_taxpayer_type]",
        position: "bottom",
        content: "Set the Taxpayer Type",
        run: 'text "3"',
    });
}
});
