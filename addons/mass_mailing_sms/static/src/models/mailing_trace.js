/** @odoo-module **/

import { attr, Patch } from '@mail/model';

// ensure load order
import '@mass_mailing/models/mailing_trace';

Patch({
    name: 'MailingTrace',
    fields: {
        sms_number: attr(),
    }
});
