odoo.define('l10n_ar.account_tour', function (require) {
"use strict";

require('account.tour');
let tour = require('web_tour.tour');

let account_tour = tour.tours.account_tour;

if (account_tour.extra && (account_tour.extra.company_account_fiscal_country_code || "") === 'AR') {
    // Configure the AFIP Responsibility
    let partner_step_idx = _.findIndex(account_tour.steps, step => step.trigger === 'div[name=partner_id] input');
    account_tour.steps.splice(partner_step_idx + 2, 0, {
        trigger: "div[name=l10n_ar_afip_responsibility_type_id] input",
        extra_trigger: "[name=move_type][raw-value=out_invoice]",
        position: "bottom",
        content: "Set the AFIP Responsability",
        run: "text IVA",
    }, {
        trigger: ".ui-menu-item > a:contains('IVA').ui-state-active",
        auto: true,
        in_modal: false,
    });
}
});
