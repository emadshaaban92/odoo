odoo.define("website.tour.website_edit_save", function (require) {
"use strict";

const tour = require("web_tour.tour");

tour.register("test_edit_save", {
    test: true,
    url: "/test_unchanged",
}, [{
    content: "Enter edit mode",
    trigger: 'a[data-action=edit]',
}, {
    content: "Save",
    trigger: '[data-action="save"]',
}]);
});
