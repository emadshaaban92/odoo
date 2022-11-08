/** @odoo-module alias=website.homepage_edit_discard*/
"use strict";

import wTourUtils from "website.tour_utils";

wTourUtils.registerWebsitePreviewTour('homepage_edit_discard', {
    url: '/',
    edition: true,
    test: true
}, [{
    trigger: "#oe_snippets button[data-action=\"cancel\"]:not([disabled])",
    extra_trigger: "body:not(:has(.o_dialog))",
    content: "<b>Click Discard</b> to Discard all Changes.",
    position: "bottom",
}, {
    trigger: "iframe body:not(.editor_enable)",
    run: () => null,
}]);
