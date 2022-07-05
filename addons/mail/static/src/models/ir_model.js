/** @odoo-module **/

import { registerModel } from '@mail/model/model_core';
import { attr } from '@mail/model/model_field';

/**
 * Mirrors the fields of the python model ir.model.
 */
registerModel({
    name: 'ir.model',
    identifyingFields: ['id'],
    fields: {
        id: attr({
            readonly: true,
            required: true,
        }),
        is_mail_thread: attr({
            default: false,
        }),
        is_mail_activity: attr({
            default: false,
        }),
        model: attr({}),
    },
});
