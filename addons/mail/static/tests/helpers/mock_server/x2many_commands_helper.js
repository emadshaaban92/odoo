/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { MockServer } from "@web/../tests/helpers/mock_server";
import { x2ManyCommands } from "@web/core/orm_service";

patch(MockServer.prototype, "mail.MockServer", {
    x2ManyCreate: function(id, values) {
        if (!Number.isInteger(id)) {
            values = id;
            id = 0;
        }
        return x2ManyCommands.create(id, values);
    },
    x2ManyUpdate: x2ManyCommands.update,
    x2ManyDelete: x2ManyCommands.delete,
    x2ManyForget: x2ManyCommands.forget,
    x2ManyLinkTo: x2ManyCommands.linkTo,
    x2ManyDeleteAll: x2ManyCommands.deleteAll,
    x2ManyReplaceWith: x2ManyCommands.replaceWith,
});
