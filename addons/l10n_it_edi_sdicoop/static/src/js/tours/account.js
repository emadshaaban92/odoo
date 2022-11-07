odoo.define('l10n_it_edi_sdicoop.account_tour', function (require) {
"use strict";

require('account.tour');
var core = require('web.core');
let tour = require('web_tour.tour');

var _t = core._t;

let account_tour = tour.tours.account_tour;

if (account_tour.extra && (account_tour.extra.company_account_fiscal_country_code || "") === 'IT') {
    // Accept the terms and conditions in the settings to use FatturaPA.
    let document_save_step_idx = _.findIndex(account_tour.steps, step => step.trigger === 'button[name=document_layout_save]');
    account_tour.steps.splice(document_save_step_idx + 1, 0, {
        trigger: 'button[data-menu-xmlid="account.menu_finance_configuration"]',
        content: _t("Let's accept the terms and conditions in the settings to use FatturaPA."),
        position: "bottom",
        run: "click",
    }, {
        trigger: 'a[data-menu-xmlid="account.menu_account_config"]',
        content: _t("Open the Settings."),
        position: "right",
        run: "click",
    }, {
        trigger: "div[name=l10n_it_edi_sdicoop_register] input",
        position: "right",
        content: _t('Accept the terms.'),
        run: "click",
    }, {
        trigger: "button[name=execute]",
        position: "right",
        content: _t('Save the changes.'),
        run: "click",
    }, {
        trigger: 'a[data-menu-xmlid="account.menu_finance"], a[data-menu-xmlid="account_accountant.menu_accounting"]',
        extra_trigger: 'body:not(:has(span:contains("Unsaved changes")))',
        content: _t("Go back to dashboard."),
        position: "bottom",
        run: "click",
    });
}
});
