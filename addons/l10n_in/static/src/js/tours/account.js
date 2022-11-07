odoo.define('l10n_in.account_tour', function (require) {
"use strict";

require('account.tour');
var core = require('web.core');
let tour = require('web_tour.tour');

var _t = core._t;

let account_tour = tour.tours.account_tour;

if (account_tour.extra && (account_tour.extra.company_account_fiscal_country_code || "") === 'IN') {
    // Accept the terms and conditions in the settings to use FatturaPA.
    let add_line_step_idx = _.findIndex(account_tour.steps, step => step.trigger === 'div[name=invoice_line_ids] .o_field_x2many_list_row_add a:not([data-context])');
    account_tour.steps.splice(add_line_step_idx, 0, {
        trigger: "select[name=l10n_in_gst_treatment]",
        extra_trigger: "body:not(.modal-open)",
        position: "bottom",
        content: "Set the GST Treatment",
        in_modal: false,
        run: 'text "consumer"',
    });
}
});
