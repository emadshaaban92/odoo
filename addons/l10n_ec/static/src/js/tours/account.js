odoo.define('l10n_ec.account_tour', function (require) {
"use strict";
require('account.tour');
let tour = require('web_tour.tour');
let account_tour = tour.tours.account_tour;
if (account_tour.extra && (account_tour.extra.company_account_fiscal_country_code || "") === 'EC') {
    // Configure the Document Number: In case there isn't already a posted invoice,
    // the document number will not be set automaticly and therefore should be manually set.
    let confirm_step_idx = _.findIndex(account_tour.steps, step => step.trigger === 'button[name=action_post]');
    account_tour.steps.splice(confirm_step_idx - 1, 0, {
        trigger: "div[name=l10n_latam_document_type_id]",
        auto: true,
        in_modal: false,
        run: function () {
            $('input[name="l10n_latam_document_number"]').val('001-001-123456789').trigger('change');
        }
    });
}
});
